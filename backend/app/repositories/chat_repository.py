from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import Chat


class ChatRepository:

    def create(self, db: Session, chat: Chat) -> Chat:
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def get_by_id(self, db: Session, chat_id: int) -> Chat | None:
        stmt = select(Chat).where(Chat.id == chat_id)
        return db.scalar(stmt)

    def get_all_by_document(self, db: Session, document_id: int) -> list[Chat]:
        stmt = (
            select(Chat)
            .where(Chat.document_id == document_id)
            .order_by(Chat.created_at.desc())
        )
        return list(db.scalars(stmt).all())

    def update(self, db: Session, chat: Chat) -> Chat:
        db.commit()
        db.refresh(chat)
        return chat
