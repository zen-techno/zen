from logging import getLogger
from uuid import UUID

from src.core.unit_of_work import AbstractUnitOfWork
from src.exceptions.repositories import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.exceptions.services import (
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)
from src.schemas.users import UserReadSchema, UserUpdateSchema

logger = getLogger("UserService")


class UserService:
    @staticmethod
    async def get_all_users(*, uow: AbstractUnitOfWork) -> list[UserReadSchema]:
        try:
            async with uow:
                users = await uow.users.get_all()
                return [user.to_read_schema() for user in users]

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def get_user_by_id(
        *, uow: AbstractUnitOfWork, user_id: UUID
    ) -> UserReadSchema:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError
                return user.to_read_schema()

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @staticmethod
    async def update_user_by_id(
        *, uow: AbstractUnitOfWork, user_id: UUID, user: UserUpdateSchema
    ) -> UserReadSchema:
        user_dict = user.model_dump()
        try:
            async with uow:
                updated_user = await uow.users.update_one(
                    id=user_id, data=user_dict
                )
                await uow.commit()
                return updated_user.to_read_schema()

        except RepositoryDoesNotExistError as exc:
            logger.exception(exc)
            raise UserServiceNotFoundError from exc
        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc
