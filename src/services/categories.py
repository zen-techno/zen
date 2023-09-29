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
    UserCategoryUpdateSchema,
    UserCategoryCreateSchema,
)
from src.services.exceptions import (
    CategoryServiceNotFoundError,
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)

category_logger = getLogger("CategoryService")
user_category_logger = getLogger("UserCategoryService")


class CategoryService:
    @staticmethod
    async def get_all_categories(
        *, uow: AbstractUnitOfWork
    ) -> list[CategoryReadSchema]:
        try:
            async with uow:
                return await uow.categories.get_all()

        except RepositoryError as exc:
            category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def get_category_by_id(
        *, uow: AbstractUnitOfWork, category_id: UUID
    ) -> CategoryReadSchema:
        try:
            async with uow:
                category: CategoryReadSchema = await uow.categories.get_one(
                    id=category_id
                )
                if category is None:
                    await uow.rollback()
                    raise CategoryServiceNotFoundError
                return category

        except RepositoryError as exc:
            category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def create_category(
        *, uow: AbstractUnitOfWork, category: CategoryCreateSchema
    ) -> CategoryReadSchema:
        category_dict = category.model_dump()
        try:
            async with uow:
                created_category = await uow.categories.add_one(
                    data=category_dict
                )
                await uow.commit()
                return created_category

        except RepositoryIntegrityError as exc:
            category_logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def update_category_by_id(
        *,
        uow: AbstractUnitOfWork,
        category_id: UUID,
        category: CategoryUpdateSchema,
    ) -> CategoryReadSchema:
        category_dict = category.model_dump()
        try:
            async with uow:
                updated_category = await uow.categories.update_one(
                    id=category_id, data=category_dict
                )
                await uow.commit()
                return updated_category

        except RepositoryDoesNotExistError as exc:
            category_logger.exception(exc)
            raise CategoryServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            category_logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def delete_category_by_id(
        *, uow: AbstractUnitOfWork, category_id: UUID
    ) -> None:
        try:
            async with uow:
                await uow.categories.delete_one(id=category_id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            category_logger.exception(exc)
            raise CategoryServiceNotFoundError from exc
        except RepositoryError as exc:
            category_logger.exception(exc)
            raise ServiceError from exc


class UserCategoryService:
    @staticmethod
    async def get_user_all_categories(
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
            user_category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def get_user_category_by_id(
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
            user_category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def create_user_category(
        *,
        uow: AbstractUnitOfWork,
        user_id: UUID,
        category: UserCategoryCreateSchema,
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
            user_category_logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            user_category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def update_user_category_by_id(
        *,
        uow: AbstractUnitOfWork,
        category_id: UUID,
        category: UserCategoryUpdateSchema,
        user_id: UUID,
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
            user_category_logger.exception(exc)
            raise CategoryServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            user_category_logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            user_category_logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def delete_user_category_by_id(
        *, uow: AbstractUnitOfWork, category_id: UUID, user_id: UUID
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
            user_category_logger.exception(exc)
            raise CategoryServiceNotFoundError from exc
        except RepositoryError as exc:
            user_category_logger.exception(exc)
            raise ServiceError from exc
