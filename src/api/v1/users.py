from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import (
    UnitOfWorkDepends,
    get_current_user,
    get_owner_user,
)
from src.schemas.users import (
    UserDetailReadSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from src.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserDetailReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_current_user(
    user: UserDetailReadSchema = Depends(get_current_user),
) -> UserDetailReadSchema:
    return user


@router.get(
    "/{user_id}",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Getting a specific user",
    dependencies=[Depends(get_owner_user)],
)
async def get_user_by_id(
    uow: UnitOfWorkDepends, user_id: UUID
) -> UserReadSchema:
    return await UserService.get_user_by_id(uow=uow, user_id=user_id)


@router.put(
    "/{user_id}",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating a specific user",
    dependencies=[Depends(get_owner_user)],
)
async def update_user_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    user: UserUpdateSchema,
) -> UserReadSchema:
    return await UserService.update_user_by_id(
        uow=uow, user_id=user_id, user=user
    )
