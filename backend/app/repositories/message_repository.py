from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    def create(self, db: Session, message: Message) -> Message:
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_all_by_chat(self, db: Session, chat_id: int) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
        )
        return list(db.scalars(stmt).all())
