from uuid import UUID

from src.core.repository import AbstractRepository
from src.schemas.categories import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, category_repository: type[AbstractRepository]):
        self.category_repository: AbstractRepository = category_repository()

    async def create_category(
        self, *, category: CategoryCreateSchema
    ) -> CategoryReadSchema:
        user_dict = category.model_dump()
        category = await self.category_repository.add_one(data=user_dict)
        return category

    async def get_all_categories(self) -> list[CategoryReadSchema]:
        return await self.category_repository.get_all()

    async def get_category_by_id(self, *, id: UUID) -> CategoryReadSchema:
        return await self.category_repository.get_one(id=id)

    async def update_category_by_id(
        self, *, id: UUID, category: CategoryUpdateSchema
    ) -> CategoryReadSchema:
        user_dict = category.model_dump()
        return await self.category_repository.update_one(id=id, data=user_dict)

    async def delete_category_by_id(self, *, id: UUID) -> None:
        await self.category_repository.delete_one(id=id)
