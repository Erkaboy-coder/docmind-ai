from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    def create(self, db: Session, document: Document) -> Document:
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def get_by_id(self, db: Session, document_id: int) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)
        return db.scalar(stmt)

    def get_all_by_user(self, db: Session, user_id: int) -> list[Document]:
        stmt = select(Document).where(Document.user_id == user_id)
        return list(db.scalars(stmt).all())

    def update(self, db: Session, document: Document) -> Document:
        db.commit()
        db.refresh(document)
        return document
