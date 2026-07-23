from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatResponse(BaseModel):
    id: int
    title: str
    document_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class SendMessageRequest(BaseModel):
    content: str


class SendMessageResponse(BaseModel):
    message: MessageResponse
    sources: list[str]
