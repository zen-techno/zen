from uuid import UUID

from src.core.repository.exceptions import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.core.unit_of_work import AbstractUnitOfWork
from src.schemas.users import UserCreateSchema, UserReadSchema, UserUpdateSchema
from src.services.exceptions import (
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)


class UserService:
    @staticmethod
    async def get_all_users(*, uow: AbstractUnitOfWork) -> list[UserReadSchema]:
        try:
            async with uow:
                return await uow.users.get_all()

        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def get_user_by_id(
        *, uow: AbstractUnitOfWork, id: UUID
    ) -> UserReadSchema:
        try:
            async with uow:
                user: UserReadSchema = await uow.users.get_one(id=id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError
                return user

        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def create_user(
        *, uow: AbstractUnitOfWork, user: UserCreateSchema
    ) -> UserReadSchema:
        user_dict = user.model_dump()
        try:
            async with uow:
                created_user = await uow.users.add_one(data=user_dict)
                await uow.commit()
                return created_user

        except RepositoryIntegrityError as exc:
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def update_user_by_id(
        *, uow: AbstractUnitOfWork, id: UUID, user: UserUpdateSchema
    ) -> UserReadSchema:
        user_dict = user.model_dump()
        try:
            async with uow:
                updated_user = await uow.users.update_one(id=id, data=user_dict)
                await uow.commit()
                return updated_user

        except RepositoryDoesNotExistError as exc:
            raise UserServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            raise ServiceError from exc

    @staticmethod
    async def delete_user_by_id(*, uow: AbstractUnitOfWork, id: UUID) -> None:
        try:
            async with uow:
                await uow.users.delete_one(id=id)
                await uow.commit()

        except RepositoryDoesNotExistError as exc:
            raise UserServiceNotFoundError from exc
        except RepositoryError as exc:
            raise ServiceError from exc
