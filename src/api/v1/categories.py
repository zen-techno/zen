from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import UnitOfWorkDepends
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)
from src.services import CategoryService

router = APIRouter(prefix="/users/{user_id}/categories", tags=["Category"])


@router.get(
    "",
    response_model=list[CategoryReadSchema],
    status_code=status.HTTP_200_OK,
    summary="Getting all categories for a specific user",
)
async def get_categories(
    uow: UnitOfWorkDepends, user_id: UUID
) -> list[CategoryReadSchema]:
    return await CategoryService.get_all_categories(uow=uow, user_id=user_id)


@router.get(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Getting a category for a specific user",
)
async def get_category_by_id(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID
) -> CategoryReadSchema:
    return await CategoryService.get_category_by_id(
        uow=uow, user_id=user_id, category_id=category_id
    )


@router.post(
    "",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Creating a category for a specific user",
)
async def add_category(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category: CategoryCreateSchema,
) -> CategoryReadSchema:
    return await CategoryService.create_category(
        uow=uow, user_id=user_id, category=category
    )


@router.put(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating a category for a specific user",
)
async def update_category_by_id(
    uow: UnitOfWorkDepends,
    user_id: UUID,
    category_id: UUID,
    category: CategoryUpdateSchema,
) -> CategoryReadSchema:
    return await CategoryService.update_category_by_id(
        uow=uow, user_id=user_id, category_id=category_id, category=category
    )


@router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a category for a specific user",
)
async def remove_category_by_id(
    uow: UnitOfWorkDepends, user_id: UUID, category_id: UUID
) -> None:
    await CategoryService.delete_category_by_id(
        uow=uow, user_id=user_id, category_id=category_id
    )
