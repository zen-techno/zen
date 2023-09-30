from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, PositiveInt


class ExpenseReadSchema(BaseModel):
    id: UUID
    name: str
    amount: PositiveInt
    transaction_at: datetime


class ExpenseCreateSchema(BaseModel):
    name: str
    amount: PositiveInt


class ExpenseUpdateSchema(BaseModel):
    name: str
    amount: PositiveInt
