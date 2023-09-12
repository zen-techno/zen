from uuid import UUID

from src.core.repository import AbstractRepository
from src.schemas.users import UserCreateSchema, UserReadSchema, UserUpdateSchema


class UserService:
    def __init__(self, user_repository: type[AbstractRepository]):
        self.user_repository: AbstractRepository = user_repository()

    async def create_user(self, *, user: UserCreateSchema) -> UserReadSchema:
        user_dict = user.model_dump()
        user = await self.user_repository.add_one(data=user_dict)
        return user

    async def get_all_users(self) -> list[UserReadSchema]:
        return await self.user_repository.get_all()

    async def get_user_by_id(self, *, id: UUID) -> UserReadSchema:
        return await self.user_repository.get_one(id=id)

    async def update_user_by_id(
        self, *, id: UUID, user: UserUpdateSchema
    ) -> UserReadSchema:
        user_dict = user.model_dump()
        return await self.user_repository.update_one(id=id, data=user_dict)

    async def delete_user_by_id(self, *, id: UUID) -> None:
        await self.user_repository.delete_one(id=id)
