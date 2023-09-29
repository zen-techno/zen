from uuid import UUID

from pydantic import BaseModel


class CategoryReadSchema(BaseModel):
    id: UUID
    name: str
    user_id: UUID


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str
