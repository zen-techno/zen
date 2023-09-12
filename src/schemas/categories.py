from uuid import UUID

from pydantic import BaseModel


class CategoryReadSchema(BaseModel):
    id: UUID
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str
