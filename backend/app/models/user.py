from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )
    chats = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete"
    )

    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )