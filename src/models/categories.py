from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.categories import CategoryReadSchema


class Category(Base):
    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"

    def to_read_model(self) -> CategoryReadSchema:
        return CategoryReadSchema(id=self.id, name=self.name)
