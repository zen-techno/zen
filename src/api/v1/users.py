from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import UnitOfWorkDepends
from src.schemas.users import UserCreateSchema, UserReadSchema, UserUpdateSchema
from src.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserReadSchema],
    status_code=status.HTTP_200_OK,
    summary="Getting all users",
)
async def get_users(uow: UnitOfWorkDepends) -> list[UserReadSchema]:
    return await UserService.get_all_users(uow=uow)


@router.get(
    "/{user_id}",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Getting a specific user",
)
async def get_user_by_id(
    uow: UnitOfWorkDepends, user_id: UUID
) -> UserReadSchema:
    return await UserService.get_user_by_id(uow=uow, user_id=user_id)


@router.post(
    "",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Creating a user",
)
async def add_user(
    uow: UnitOfWorkDepends, user: UserCreateSchema
) -> UserReadSchema:
    return await UserService.create_user(uow=uow, user=user)


@router.put(
    "/{user_id}",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating a specific user",
)
async def update_user_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    user: UserUpdateSchema,
) -> UserReadSchema:
    return await UserService.update_user_by_id(
        uow=uow, user_id=user_id, user=user
    )


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a specific user",
)
async def remove_user_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
) -> None:
    await UserService.delete_user_by_id(uow=uow, user_id=user_id)
