from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dataclasses import User
from src.models.base import DeclarativeBase


class UserModel(DeclarativeBase):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    expenses: Mapped[list["ExpenseModel"]] = relationship(
        back_populates="who_paid"
    )
    categories: Mapped[list["CategoryModel"]] = relationship(
        back_populates="user"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    def to_dataclass(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            telegram_id=self.telegram_id,
            password=self.password,
            registered_at=self.registered_at,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
        )
