from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dataclasses import Category
from src.models.base import DeclarativeBase


class CategoryModel(DeclarativeBase):
    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    user: Mapped["UserModel"] = relationship(back_populates="categories")
    expenses: Mapped[list["ExpenseModel"]] = relationship(
        back_populates="category"
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"

    def to_dataclass(self) -> Category:
        return Category(id=self.id, name=self.name, user_id=self.user_id)
