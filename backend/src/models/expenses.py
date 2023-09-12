from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.models.base import Base
from backend.src.schemas.categories import CategoryReadSchema
from backend.src.schemas.expenses import ExpenseReadSchema
from backend.src.schemas.users import UserReadSchema


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
    who_paid_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("category.id", ondelete="RESTRICT"), nullable=False
    )

    who_paid: Mapped["User"] = relationship(back_populates="expenses")
    category: Mapped["Category"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id!r}, name={self.name!r}, amount={self.name!r})"
        )

    def to_read_model(self) -> ExpenseReadSchema:
        return ExpenseReadSchema(
            id=self.id,
            name=self.name,
            amount=self.amount,
            transaction_date=self.transaction_date,
            who_paid=UserReadSchema(
                id=self.who_paid.id,
                name=self.who_paid.name,
                telegram_id=self.who_paid.telegram_id,
            ),
            category=CategoryReadSchema(
                id=self.category.id, name=self.category.name
            ),
        )
