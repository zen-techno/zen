from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.src.api.dependencies import (
    CategoryServiceDepends,
    valid_category_uuid,
)
from backend.src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryReadSchema])
async def get_categories(
    category_service: CategoryServiceDepends,
) -> List[CategoryReadSchema]:
    return await category_service.get_all_categories()


@router.get("/{uuid}", response_model=CategoryReadSchema)
async def get_category_by_uuid(
    valid_category: CategoryReadSchema = Depends(valid_category_uuid),
) -> CategoryReadSchema:
    return valid_category


@router.post("/", response_model=CategoryReadSchema)
async def add_category(
    category: CategoryCreateSchema, category_service: CategoryServiceDepends
):
    return await category_service.create_category(category=category)


@router.put(
    "/{uuid}",
    response_model=CategoryReadSchema,
    dependencies=[Depends(valid_category_uuid)],
)
async def update_category(
    uuid: UUID,
    category: CategoryUpdateSchema,
    category_service: CategoryServiceDepends,
) -> CategoryReadSchema:
    return await category_service.update_category_by_uuid(
        id_=uuid, category=category
    )


@router.delete(
    "/{uuid}", response_model=None, dependencies=[Depends(valid_category_uuid)]
)
async def remove_category_by_uuid(
    uuid: UUID, category_service: CategoryServiceDepends
) -> None:
    await category_service.delete_category(id_=uuid)
