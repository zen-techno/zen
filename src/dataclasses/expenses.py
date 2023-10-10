from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.schemas.expenses import ExpenseReadSchema


@dataclass(frozen=True, slots=True)
class Expense:
    id: UUID
    name: str
    amount: int
    transaction_at: datetime
    who_paid_id: UUID
    category_id: UUID

    def to_read_schema(self) -> ExpenseReadSchema:
        return ExpenseReadSchema(
            id=self.id,
            name=self.name,
            amount=self.amount,
            transaction_at=self.transaction_at,
        )
