from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.src.api.dependencies import UserServiceDepends, valid_user_uuid
from backend.src.schemas.users import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserReadSchema])
async def get_users(user_service: UserServiceDepends) -> List[UserReadSchema]:
    return await user_service.get_all_users()


@router.get("/{uuid}", response_model=UserReadSchema)
async def get_user_by_uuid(
    valid_user: UserReadSchema = Depends(valid_user_uuid),
) -> UserReadSchema:
    return valid_user


@router.post("/", response_model=UserReadSchema)
async def add_user(
    user: UserCreateSchema, user_service: UserServiceDepends
) -> UserReadSchema:
    return await user_service.create_user(user=user)


@router.put(
    "/{uuid}",
    response_model=UserReadSchema,
    dependencies=[Depends(valid_user_uuid)],
)
async def update_user(
    uuid: UUID,
    user: UserUpdateSchema,
    user_service: UserServiceDepends,
) -> UserReadSchema:
    return await user_service.update_user_by_uuid(id_=uuid, user=user)


@router.delete(
    "/{uuid}", response_model=None, dependencies=[Depends(valid_user_uuid)]
)
async def remove_user_by_uuid(
    uuid: UUID, user_service: UserServiceDepends
) -> None:
    await user_service.delete_user(id_=uuid)
