from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


class UserReadSchema(BaseModel):
    id: UUID
    name: str
    telegram_id: PositiveInt | None = Field(default=None)


class UserCreateSchema(BaseModel):
    name: str
    telegram_id: PositiveInt | None = Field(default=None)


class UserUpdateSchema(BaseModel):
    name: str
    telegram_id: PositiveInt | None = Field(default=None)
