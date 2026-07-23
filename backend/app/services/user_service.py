from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password

class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(
        self,
        db: Session,
        user: UserCreate
    ) -> User:

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password)
        )

        return self.repository.create(
            db=db,
            user=db_user
        )