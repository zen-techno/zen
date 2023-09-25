from uuid import UUID

from src.core.repository.exceptions import RepositoryError, RepositoryIntegrityError, RepositoryDoesNotExistError
from src.core.unit_of_work import AbstractUnitOfWork
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)
from src.services.exceptions import ServiceError, ExpenseServiceNotFoundError, CategoryServiceNotFoundError, UserServiceNotFoundError, ServiceBadRequestError


class ExpenseService:
    @staticmethod
    async def get_all_expenses(*, uow: AbstractUnitOfWork) -> list[ExpenseReadSchema]:
        try:
            async with uow:
                return await uow.expenses.get_all()

        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def get_expense_by_id(*, uow: AbstractUnitOfWork, id: UUID) -> ExpenseReadSchema:
        try:
            async with uow:
                expense: ExpenseReadSchema = await uow.expenses.get_one(id=id)
                if expense is None:
                    await uow.rollback()
                    raise ExpenseServiceNotFoundError
                return expense

        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def create_expense(
        *, uow: AbstractUnitOfWork, expense: ExpenseCreateSchema
    ) -> ExpenseReadSchema:
        expense_dict = expense.model_dump()
        try:
            async with uow:
                is_user_exist = await uow.users.get_one(id=expense.who_paid_id)
                if not is_user_exist:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                is_category_exist = await uow.categories.get_one(id=expense.category_id)
                if not is_category_exist:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                created_expense = await uow.expenses.add_one(data=expense_dict)
                await uow.commit()
                return created_expense

        except RepositoryIntegrityError as exc:
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def update_expense_by_id(
        *, uow: AbstractUnitOfWork, id: UUID, expense: ExpenseUpdateSchema
    ) -> ExpenseReadSchema:
        expense_dict = expense.model_dump()
        try:
            async with uow:
                is_user_exist = await uow.users.get_one(id=expense.who_paid_id)
                if not is_user_exist:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                is_category_exist = await uow.categories.get_one(id=expense.category_id)
                if not is_category_exist:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                updated_expense = await uow.expenses.update_one(id=id, data=expense_dict)
                await uow.commit()
                return updated_expense

        except RepositoryDoesNotExistError as exc:
            raise ExpenseServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def delete_expense_by_id(*, uow: AbstractUnitOfWork, id: UUID) -> None:
        try:
            async with uow:
                await uow.expenses.delete_one(id=id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            raise ExpenseServiceNotFoundError from exc
        except RepositoryError as exc:
            raise ServiceError from exc
