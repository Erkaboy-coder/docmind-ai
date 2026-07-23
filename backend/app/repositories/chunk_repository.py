from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk


class ChunkRepository:

    def create_many(self, db: Session, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        db.add_all(chunks)
        db.commit()

        for chunk in chunks:
            db.refresh(chunk)

        return chunks

    def get_by_document(self, db: Session, document_id: int) -> list[DocumentChunk]:
        stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id)
        return list(db.scalars(stmt).all())
