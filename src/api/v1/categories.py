from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import CategoryServiceDepends, valid_category_id
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "", response_model=list[CategoryReadSchema], status_code=status.HTTP_200_OK
)
async def get_categories(
    category_service: CategoryServiceDepends,
) -> list[CategoryReadSchema]:
    return await category_service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_200_OK,
)
def get_category_by_id(
    valid_category: CategoryReadSchema = Depends(valid_category_id),
) -> CategoryReadSchema:
    return valid_category


@router.post(
    "", response_model=CategoryReadSchema, status_code=status.HTTP_201_CREATED
)
async def add_category(
    category: CategoryCreateSchema, category_service: CategoryServiceDepends
):
    return await category_service.create_category(category=category)


@router.put(
    "/{category_id}",
    response_model=CategoryReadSchema,
    dependencies=[Depends(valid_category_id)],
    status_code=status.HTTP_200_OK,
)
async def update_category_by_id(
    category_id: UUID,
    category: CategoryUpdateSchema,
    category_service: CategoryServiceDepends,
) -> CategoryReadSchema:
    return await category_service.update_category_by_id(
        id=category_id, category=category
    )


@router.delete(
    "/{category_id}",
    response_model=None,
    dependencies=[Depends(valid_category_id)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_category_by_id(
    category_id: UUID, category_service: CategoryServiceDepends
) -> None:
    await category_service.delete_category_by_id(id=category_id)
