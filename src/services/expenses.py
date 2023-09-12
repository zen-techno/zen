from typing import List, Type
from uuid import UUID

from src.core.repository import AbstractRepository
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)


class ExpenseService:
    def __init__(self, expense_repository: Type[AbstractRepository]):
        self.expense_repository: AbstractRepository = expense_repository()

    async def create_expense(
        self, *, expense: ExpenseCreateSchema
    ) -> ExpenseReadSchema:
        user_dict = expense.model_dump()
        expense = await self.expense_repository.add_one(data=user_dict)
        return expense

    async def get_all_expenses(self) -> List[ExpenseReadSchema]:
        return await self.expense_repository.get_all()

    async def get_expense_by_id(self, *, id: UUID) -> ExpenseReadSchema:
        return await self.expense_repository.get_one(id=id)

    async def update_expense_by_id(
        self, *, id: UUID, expense: ExpenseUpdateSchema
    ) -> ExpenseReadSchema:
        user_dict = expense.model_dump()
        return await self.expense_repository.update_one(id=id, data=user_dict)

    async def delete_expense_by_id(self, *, id: UUID) -> None:
        await self.expense_repository.delete_one(id=id)
