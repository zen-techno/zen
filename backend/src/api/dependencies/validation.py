from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException

from backend.src.api.dependencies.services import (
    CategoryServiceDepends,
    UserServiceDepends,
)
from backend.src.schemas.categories import CategoryReadSchema
from backend.src.schemas.users import UserReadSchema


async def valid_user_uuid(
    uuid: UUID, user_service: UserServiceDepends
) -> UserReadSchema:
    user = await user_service.get_user_by_uuid(id_=uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )
    return user


async def valid_category_uuid(
    uuid: UUID, category_service: CategoryServiceDepends
) -> CategoryReadSchema:
    category = await category_service.get_category_by_uuid(id_=uuid)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category is not found",
        )
    return category
