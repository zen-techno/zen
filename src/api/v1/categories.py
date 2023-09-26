from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import UnitOfWorkDepends
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)
from src.services import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "", response_model=list[CategoryReadSchema], status_code=status.HTTP_200_OK
)
async def get_categories(uow: UnitOfWorkDepends) -> list[CategoryReadSchema]:
    return await CategoryService.get_all_categories(uow=uow)


@router.get(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    uow: UnitOfWorkDepends, category_id: UUID
) -> CategoryReadSchema:
    return await CategoryService.get_category_by_id(uow=uow, id=category_id)


@router.post(
    "", response_model=CategoryReadSchema, status_code=status.HTTP_201_CREATED
)
async def add_category(
    uow: UnitOfWorkDepends,
    category: CategoryCreateSchema,
) -> CategoryReadSchema:
    return await CategoryService.create_category(uow=uow, category=category)


@router.put(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
)
async def update_category_by_id(
    uow: UnitOfWorkDepends,
    category_id: UUID,
    category: CategoryUpdateSchema,
) -> CategoryReadSchema:
    return await CategoryService.update_category_by_id(
        uow=uow, id=category_id, category=category
    )


@router.delete(
    "/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_category_by_id(
    uow: UnitOfWorkDepends, category_id: UUID
) -> None:
    await CategoryService.delete_category_by_id(uow=uow, id=category_id)
