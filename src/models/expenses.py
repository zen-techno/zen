from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dataclasses import Expense
from src.models.base import DeclarativeBase


class ExpenseModel(DeclarativeBase):
    __tablename__ = "expense"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    transaction_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    who_paid_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    who_paid: Mapped["UserModel"] = relationship(back_populates="expenses")
    category: Mapped["CategoryModel"] = relationship(back_populates="expenses")

    __table_args__ = (
        CheckConstraint(sqltext="amount > 0", name="check_amount"),
    )

    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id!r}, name={self.name!r}, amount={self.name!r})"
        )

    def to_dataclass(self) -> Expense:
        return Expense(
            id=self.id,
            name=self.name,
            amount=self.amount,
            transaction_at=self.transaction_at,
            who_paid_id=self.who_paid_id,
            category_id=self.category_id,
        )
