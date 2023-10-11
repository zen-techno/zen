from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import UnitOfWorkDepends, get_owner_user
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)
from src.services import ExpenseService

router = APIRouter(
    prefix="/users/{user_id}/categories/{category_id}/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_owner_user)],
)


@router.get(
    "",
    response_model=list[ExpenseReadSchema],
    status_code=status.HTTP_200_OK,
    summary="Getting all expense records for a specific user and category",
)
async def get_expenses(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID
) -> list[ExpenseReadSchema]:
    return await ExpenseService.get_all_expenses(
        uow=uow, user_id=user_id, category_id=category_id
    )


@router.get(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Getting an expense record for a specific user and category",
)
async def get_expense_by_id(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID, expense_id: UUID
) -> ExpenseReadSchema:
    return await ExpenseService.get_expense_by_id(
        uow=uow,
        user_id=user_id,
        category_id=category_id,
        expense_id=expense_id,
    )


@router.post(
    "",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Creating an expense record for a specific user and category",
)
async def add_expense(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category_id: UUID,
    expense: ExpenseCreateSchema,
) -> ExpenseReadSchema:
    return await ExpenseService.create_expense(
        uow=uow, user_id=user_id, category_id=category_id, expense=expense
    )


@router.put(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating an expense record for a specific user and category",
)
async def update_expense_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category_id: UUID,
    expense_id: UUID,
    expense: ExpenseUpdateSchema,
) -> ExpenseReadSchema:
    return await ExpenseService.update_expense_by_id(
        uow=uow,
        user_id=user_id,
        category_id=category_id,
        expense_id=expense_id,
        expense=expense,
    )


@router.delete(
    "/{expense_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting an expense record for a specific user and category",
)
async def remove_expense_by_uuid(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID, expense_id: UUID
) -> None:
    await ExpenseService.delete_expense_by_id(
        uow=uow, user_id=user_id, category_id=category_id, expense_id=expense_id
    )
