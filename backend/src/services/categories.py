from typing import List, Type
from uuid import UUID

from backend.src.core.repository import AbstractRepository
from backend.src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, category_repository: Type[AbstractRepository]):
        self.category_repository: AbstractRepository = category_repository()

    async def create_category(
        self, *, category: CategoryCreateSchema
    ) -> CategoryReadSchema:
        user_dict = category.model_dump()
        category = await self.category_repository.add_one(data=user_dict)
        return category

    async def get_all_categories(self) -> List[CategoryReadSchema]:
        return await self.category_repository.get_all()

    async def get_category_by_uuid(self, *, id_: UUID) -> CategoryReadSchema:
        return await self.category_repository.get_one(id=id_)

    async def update_category_by_uuid(
        self, *, id_: UUID, category: CategoryUpdateSchema
    ) -> CategoryReadSchema:
        user_dict = category.model_dump()
        return await self.category_repository.update_one(
            id_=id_, data=user_dict
        )

    async def delete_category(self, *, id_: UUID) -> None:
        await self.category_repository.delete_one(id_=id_)
