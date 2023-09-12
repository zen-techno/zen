from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.users import UserReadSchema


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[Optional[int]]

    expenses: Mapped[List["Expense"]] = relationship(back_populates="who_paid")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    def to_read_model(self) -> UserReadSchema:
        return UserReadSchema(
            id=self.id, name=self.name, telegram_id=self.telegram_id
        )
