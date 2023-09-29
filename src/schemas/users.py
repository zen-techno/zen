from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, PositiveInt


class UserReadSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    registered_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool
    telegram_id: PositiveInt | None = Field(default=None)


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    telegram_id: PositiveInt | None = Field(default=None)


class UserUpdateSchema(BaseModel):
    name: str
    telegram_id: PositiveInt | None = Field(default=None)
