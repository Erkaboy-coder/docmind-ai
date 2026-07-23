import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.ai.chunking import chunk_text
from app.ai.embeddings import embed_texts
from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.models.user import User
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.utils.text_extractor import extract_text

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()
        self.chunk_repository = ChunkRepository()

    def upload_document(
        self,
        db: Session,
        user: User,
        file: UploadFile
    ) -> Document:

        extension = (
            file.filename.rsplit(".", 1)[-1].lower()
            if file.filename and "." in file.filename
            else ""
        )

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Faqat PDF, DOCX yoki TXT fayllar qabul qilinadi"
            )

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        stored_name = f"{uuid.uuid4().hex}.{extension}"
        stored_path = UPLOAD_DIR / stored_name

        with open(stored_path, "wb") as buffer:
            buffer.write(file.file.read())

        document = Document(
            user_id=user.id,
            filename=file.filename,
            file_path=str(stored_path),
            file_type=extension,
            status="uploaded"
        )

        document = self.repository.create(
            db=db,
            document=document
        )

        try:
            document.content = extract_text(stored_path, extension)
            self._index(db, document)
            document.status = "ready"
        except Exception:
            document.status = "failed"

        return self.repository.update(
            db=db,
            document=document
        )

    def _index(self, db: Session, document: Document) -> None:
        chunks = chunk_text(document.content or "")

        if not chunks:
            return

        embeddings = embed_texts(chunks)

        chunk_rows = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding
            )
            for index, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]

        self.chunk_repository.create_many(db, chunk_rows)

    def list_documents(
        self,
        db: Session,
        user: User
    ) -> list[Document]:

        return self.repository.get_all_by_user(
            db=db,
            user_id=user.id
        )

    def delete_document(self, db: Session, document: Document) -> None:
        Path(document.file_path).unlink(missing_ok=True)
        self.repository.delete(db, document)
