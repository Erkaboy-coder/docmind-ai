from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()

service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return service.login(
        db=db,
        data=data
    )