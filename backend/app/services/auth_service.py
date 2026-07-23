from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password
from app.utils.jwt import create_access_token


class AuthService:

    def __init__(self):
        self.repository = UserRepository()

    def login(
        self,
        db: Session,
        data: LoginRequest
    ):

        user = self.repository.get_by_email(
            db,
            data.email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }