from logging import getLogger
from uuid import UUID

from src.core.repository.exceptions import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.core.unit_of_work import AbstractUnitOfWork
from src.schemas.expenses import (
    ExpenseCreateSchema,
    ExpenseReadSchema,
    ExpenseUpdateSchema,
)
from src.services.exceptions import (
    CategoryServiceNotFoundError,
    ExpenseServiceNotFoundError,
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)

logger = getLogger("ExpenseService")


class ExpenseService:
    @staticmethod
    async def get_all_expenses(
        *, uow: AbstractUnitOfWork, user_id: UUID, category_id: UUID
    ) -> list[ExpenseReadSchema]:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                return await uow.expenses.get_all(who_paid_ids=user_id)

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def get_expense_by_id(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
        expense_id: UUID,
    ) -> ExpenseReadSchema:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                expense: ExpenseReadSchema = await uow.expenses.get_one(
                    id=expense_id, who_paid_id=user_id, category_id=category_id
                )
                if expense is None:
                    await uow.rollback()
                    raise ExpenseServiceNotFoundError
                return expense

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def create_expense(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
        expense: ExpenseCreateSchema,
    ) -> ExpenseReadSchema:
        expense_dict = expense.model_dump()
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                created_expense = await uow.expenses.add_one(
                    data={
                        **expense_dict,
                        "who_paid_id": user_id,
                        "category_id": category_id,
                    }
                )
                await uow.commit()
                return created_expense

        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def update_expense_by_id(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
        expense_id: UUID,
        expense: ExpenseUpdateSchema,
    ) -> ExpenseReadSchema:
        expense_dict = expense.model_dump()
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                updated_expense = await uow.expenses.update_one(
                    id=expense_id,
                    data={
                        **expense_dict,
                        "who_paid_id": user_id,
                        "category_id": category_id,
                    },
                )
                await uow.commit()
                return updated_expense

        except RepositoryDoesNotExistError as exc:
            raise ExpenseServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def delete_expense_by_id(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
        expense_id: UUID,
    ) -> None:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError

                await uow.expenses.delete_one(id=expense_id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            raise ExpenseServiceNotFoundError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc
