from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import UnitOfWorkDepends
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
    UserCategoryCreateSchema,
    UserCategoryUpdateSchema
)
from src.services.categories import UserCategoryService

user_categories_router = APIRouter(
    prefix="/users/{user_id}/categories", tags=["Users"]
)


@user_categories_router.get(
    "",
    response_model=list[CategoryReadSchema],
    status_code=status.HTTP_200_OK,
    summary="Getting a category for a specific user",
)
async def get_user_categories(
    uow: UnitOfWorkDepends, user_id: UUID
) -> list[CategoryReadSchema]:
    return await UserCategoryService.get_user_all_categories(
        uow=uow, user_id=user_id
    )


@user_categories_router.get(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Getting all categories for a specific user",
)
async def get_user_category_by_id(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID
) -> CategoryReadSchema:
    return await UserCategoryService.get_user_category_by_id(
        uow=uow, category_id=category_id, user_id=user_id
    )


@user_categories_router.post(
    "",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Creating a category for a specific user",
)
async def add_user_category(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category: UserCategoryCreateSchema,
) -> CategoryReadSchema:
    return await UserCategoryService.create_user_category(
        uow=uow, category=category, user_id=user_id
    )


@user_categories_router.put(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating a category for a specific user",
)
async def update_user_category_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category_id: UUID,
    category: UserCategoryUpdateSchema,
) -> CategoryReadSchema:
    return await UserCategoryService.update_user_category_by_id(
        uow=uow, category_id=category_id, category=category, user_id=user_id
    )


@user_categories_router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a category for a specific user",
)
async def remove_user_category_by_id(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID
) -> None:
    await UserCategoryService.delete_user_category_by_id(
        uow=uow, category_id=category_id, user_id=user_id
    )


router = APIRouter(tags=["Categories"])


registered_routers = [
    user_categories_router,
]

for rout in registered_routers:
    router.include_router(rout)
