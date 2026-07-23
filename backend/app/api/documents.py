from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.schemas.qa import AskRequest, AskResponse
from app.services.document_service import DocumentService
from app.services.qa_service import QAService

router = APIRouter()

service = DocumentService()
qa_service = QAService()


@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.upload_document(
        db=db,
        user=current_user,
        file=file
    )


@router.get(
    "/documents",
    response_model=list[DocumentResponse]
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.list_documents(
        db=db,
        user=current_user
    )


@router.post(
    "/documents/{document_id}/ask",
    response_model=AskResponse
)
def ask_document(
    document_id: int,
    data: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = service.repository.get_by_id(db, document_id)

    if document is None or document.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hujjat topilmadi")

    return qa_service.ask(
        db=db,
        document=document,
        question=data.question
    )
