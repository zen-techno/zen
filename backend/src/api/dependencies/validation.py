from typing import TypeAlias, Union
from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException

from backend.src.api.dependencies.services import (
    CategoryServiceDepends,
    ExpenseServiceDepends,
    UserServiceDepends,
)
from backend.src.schemas.categories import CategoryReadSchema
from backend.src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)
from backend.src.schemas.users import UserReadSchema


# Users validations


async def valid_user_id(
    user_id: UUID, user_service: UserServiceDepends
) -> UUID:
    user = await user_service.get_user_by_id(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )
    return user


# Category validations


async def valid_category_id(
    category_id: UUID, category_service: CategoryServiceDepends
) -> CategoryReadSchema:
    category = await category_service.get_category_by_id(id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category is not found",
        )
    return category


# Expense validations


async def valid_expense_id(
    expense_id: UUID, expense_service: ExpenseServiceDepends
) -> ExpenseReadSchema:
    expense = await expense_service.get_expense_by_id(id=expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense is not found",
        )
    return expense


async def valid_expense_schema(
    expense: Union[ExpenseCreateSchema, ExpenseUpdateSchema],
    user_service: UserServiceDepends,
    category_service: CategoryServiceDepends,
) -> Union[ExpenseCreateSchema, ExpenseUpdateSchema]:
    user_id = expense.who_paid_id
    user = await user_service.get_user_by_id(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The user with the given id does not exist",
        )
    category_id = expense.category_id
    category = await category_service.get_category_by_id(id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The category with the given id does not exist.",
        )
    return expense
