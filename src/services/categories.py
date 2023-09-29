from logging import getLogger
from uuid import UUID

from src.core.repository.exceptions import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.core.unit_of_work import AbstractUnitOfWork
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)
from src.services.exceptions import (
    CategoryServiceNotFoundError,
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)

logger = getLogger("CategoryService")


class CategoryService:
    @staticmethod
    async def get_all_categories(
        *, uow: AbstractUnitOfWork, user_id: UUID
    ) -> list[CategoryReadSchema]:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                return await uow.categories.get_all(user_id=user_id)

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def get_category_by_id(
        *, uow: AbstractUnitOfWork, user_id: UUID, category_id: UUID
    ) -> CategoryReadSchema:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                category: CategoryReadSchema = await uow.categories.get_one(
                    id=category_id, user_id=user_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError
                return category

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def create_category(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category: CategoryCreateSchema,
    ) -> CategoryReadSchema:
        category_dict = category.model_dump()
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                created_category = await uow.categories.add_one(
                    data={**category_dict, "user_id": user_id}
                )
                await uow.commit()
                return created_category

        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def update_category_by_id(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
        category: CategoryUpdateSchema,
    ) -> CategoryReadSchema:
        category_dict = category.model_dump()
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                updated_category = await uow.categories.update_one(
                    id=category_id, data={**category_dict, "user_id": user_id}
                )
                await uow.commit()
                return updated_category

        except RepositoryDoesNotExistError as exc:
            raise CategoryServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def delete_category_by_id(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category_id: UUID,
    ) -> None:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError

                await uow.categories.delete_one(id=category_id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            raise CategoryServiceNotFoundError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc
