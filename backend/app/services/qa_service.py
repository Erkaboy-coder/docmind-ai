from sqlalchemy.orm import Session

from app.ai.embeddings import embed_text
from app.ai.ollama_client import ask_llm
from app.ai.similarity import cosine_similarity
from app.models.document import Document
from app.repositories.chunk_repository import ChunkRepository

TOP_K = 3


class QAService:

    def __init__(self):
        self.chunk_repository = ChunkRepository()

    def ask(self, db: Session, document: Document, question: str) -> dict:
        chunks = self.chunk_repository.get_by_document(db, document.id)

        if not chunks:
            return {
                "answer": "Bu hujjat hali indekslanmagan yoki undan matn topilmadi.",
                "sources": []
            }

        question_embedding = embed_text(question)

        ranked_chunks = sorted(
            chunks,
            key=lambda chunk: cosine_similarity(question_embedding, chunk.embedding),
            reverse=True
        )

        top_chunks = ranked_chunks[:TOP_K]
        context = "\n\n---\n\n".join(chunk.content for chunk in top_chunks)

        answer = ask_llm(question, context)

        return {
            "answer": answer,
            "sources": [chunk.content[:200] for chunk in top_chunks]
        }
