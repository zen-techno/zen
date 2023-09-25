from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import (
    UnitOfWorkDepends
)
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)

from src.services import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get(
    "", response_model=list[ExpenseReadSchema], status_code=status.HTTP_200_OK
)
async def get_expenses(uow: UnitOfWorkDepends) -> list[ExpenseReadSchema]:
    return await ExpenseService.get_all_expenses(uow=uow)


@router.get(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_200_OK,
)
async def get_expense_by_id(uow: UnitOfWorkDepends, expense_id: UUID) -> ExpenseReadSchema:
    return await ExpenseService.get_expense_by_id(uow=uow, id=expense_id)


@router.post(
    "", response_model=ExpenseReadSchema, status_code=status.HTTP_201_CREATED
)
async def add_expense(
    uow: UnitOfWorkDepends, expense: ExpenseCreateSchema
) -> ExpenseReadSchema:
    return await ExpenseService.create_expense(uow=uow, expense=expense)


@router.put(
    "/{expense_id}",
    response_model=ExpenseReadSchema,
    status_code=status.HTTP_200_OK,
)
async def update_expense_by_id(
    uow: UnitOfWorkDepends,
    expense_id: UUID,
    expense: ExpenseUpdateSchema
) -> ExpenseReadSchema:
    return await ExpenseService.update_expense_by_id(uow=uow, id=expense_id, expense=expense)


@router.delete(
    "/{expense_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_expense_by_uuid(
    uow: UnitOfWorkDepends, expense_id: UUID
) -> None:
    await ExpenseService.delete_expense_by_id(uow=uow, id=expense_id)
