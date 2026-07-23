from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.schemas.chat import (
    ChatResponse,
    MessageResponse,
    SendMessageRequest,
    SendMessageResponse,
)
from app.services.chat_service import ChatService

router = APIRouter()

service = ChatService()
document_repository = DocumentRepository()


@router.post(
    "/documents/{document_id}/chats",
    response_model=ChatResponse,
    status_code=201
)
def create_chat(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = document_repository.get_by_id(db, document_id)

    if document is None or document.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hujjat topilmadi")

    return service.create_chat(
        db=db,
        user_id=current_user.id,
        document_id=document_id
    )


@router.get(
    "/documents/{document_id}/chats",
    response_model=list[ChatResponse]
)
def list_chats(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = document_repository.get_by_id(db, document_id)

    if document is None or document.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hujjat topilmadi")

    return service.list_chats(db=db, document_id=document_id)


@router.get(
    "/chats/{chat_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = service.chat_repository.get_by_id(db, chat_id)

    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Suhbat topilmadi")

    return service.get_messages(db=db, chat_id=chat_id)


@router.post(
    "/chats/{chat_id}/messages",
    response_model=SendMessageResponse
)
def send_message(
    chat_id: int,
    data: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = service.chat_repository.get_by_id(db, chat_id)

    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Suhbat topilmadi")

    return service.send_message(
        db=db,
        chat=chat,
        content=data.content
    )


@router.delete(
    "/chats/{chat_id}",
    status_code=204
)
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = service.chat_repository.get_by_id(db, chat_id)

    if chat is None or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Suhbat topilmadi")

    service.delete_chat(db=db, chat=chat)
