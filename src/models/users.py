from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.users import UserReadSchema


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    telegram_id: Mapped[int | None] = mapped_column(unique=True)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="who_paid")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint(
            sqltext="REGEXP_LIKE(email, '/^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}$/i')",
            name="check_email",
        ),
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    def to_read_model(self) -> UserReadSchema:
        return UserReadSchema(
            id=self.id, name=self.name, telegram_id=self.telegram_id
        )
