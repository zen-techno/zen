from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, PositiveInt, SecretStr


class UserReadSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    telegram_id: PositiveInt


class UserDetailReadSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    telegram_id: PositiveInt
    registered_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    telegram_id: PositiveInt
    password: SecretStr


class UserUpdateSchema(BaseModel):
    name: str
    telegram_id: PositiveInt
