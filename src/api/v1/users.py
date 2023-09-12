from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import UserServiceDepends, valid_user_id
from src.schemas.users import UserCreateSchema, UserReadSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "", response_model=List[UserReadSchema], status_code=status.HTTP_200_OK
)
async def get_users(user_service: UserServiceDepends) -> List[UserReadSchema]:
    return await user_service.get_all_users()


@router.get(
    "/{user_id}", response_model=UserReadSchema, status_code=status.HTTP_200_OK
)
def get_user_by_id(
    valid_user: UserReadSchema = Depends(valid_user_id),
) -> UserReadSchema:
    return valid_user


@router.post(
    "/", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def add_user(
    user: UserCreateSchema, user_service: UserServiceDepends
) -> UserReadSchema:
    return await user_service.create_user(user=user)


@router.put(
    "/{user_id}",
    response_model=UserReadSchema,
    dependencies=[Depends(valid_user_id)],
    status_code=status.HTTP_200_OK,
)
async def update_user_by_id(
    user_id: UUID,
    user: UserUpdateSchema,
    user_service: UserServiceDepends,
) -> UserReadSchema:
    return await user_service.update_user_by_id(id=user_id, user=user)


@router.delete(
    "/{user_id}",
    response_model=None,
    dependencies=[Depends(valid_user_id)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_by_id(
    user_id: UUID, user_service: UserServiceDepends
) -> None:
    await user_service.delete_user_by_id(id=user_id)
