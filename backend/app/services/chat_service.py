from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.message import Message
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.services.qa_service import QAService


class ChatService:

    def __init__(self):
        self.chat_repository = ChatRepository()
        self.message_repository = MessageRepository()
        self.qa_service = QAService()

    def create_chat(self, db: Session, user_id: int, document_id: int) -> Chat:
        chat = Chat(
            user_id=user_id,
            document_id=document_id,
            title="Yangi suhbat"
        )
        return self.chat_repository.create(db, chat)

    def list_chats(self, db: Session, document_id: int) -> list[Chat]:
        return self.chat_repository.get_all_by_document(db, document_id)

    def delete_chat(self, db: Session, chat: Chat) -> None:
        self.chat_repository.delete(db, chat)

    def get_messages(self, db: Session, chat_id: int) -> list[Message]:
        return self.message_repository.get_all_by_chat(db, chat_id)

    def send_message(self, db: Session, chat: Chat, content: str) -> dict:
        existing_messages = self.message_repository.get_all_by_chat(db, chat.id)

        if not existing_messages:
            chat.title = content[:60]
            self.chat_repository.update(db, chat)

        user_message = Message(
            chat_id=chat.id,
            role="user",
            content=content
        )
        self.message_repository.create(db, user_message)

        result = self.qa_service.ask(db, chat.document, content)

        assistant_message = Message(
            chat_id=chat.id,
            role="assistant",
            content=result["answer"]
        )
        self.message_repository.create(db, assistant_message)

        return {
            "message": assistant_message,
            "sources": result["sources"]
        }
