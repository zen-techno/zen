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
)


class CategoryService:
    @staticmethod
    async def get_all_categories(
        *, uow: AbstractUnitOfWork
    ) -> list[CategoryReadSchema]:
        try:
            async with uow:
                return await uow.categories.get_all()

        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def get_category_by_id(
        *, uow: AbstractUnitOfWork, id: UUID
    ) -> CategoryReadSchema:
        try:
            async with uow:
                category = await uow.categories.get_one(id=id)
                if category is None:
                    raise CategoryServiceNotFoundError
                return category

        except RepositoryError as exc:
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
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def update_category_by_id(
        *, uow: AbstractUnitOfWork, id: UUID, category: CategoryUpdateSchema
    ) -> CategoryReadSchema:
        category_dict = category.model_dump()
        try:
            async with uow:
                updated_category = await uow.categories.update_one(
                    id=id, data=category_dict
                )
                await uow.commit()
                return updated_category

        except RepositoryDoesNotExistError as exc:
            raise CategoryServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def delete_category_by_id(
        *, uow: AbstractUnitOfWork, id: UUID
    ) -> None:
        try:
            async with uow:
                await uow.categories.delete_one(id=id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            raise CategoryServiceNotFoundError from exc
        except RepositoryError as exc:
            raise ServiceError from exc
