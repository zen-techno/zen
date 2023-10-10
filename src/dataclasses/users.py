from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.schemas.users import UserDetailReadSchema, UserReadSchema


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    name: str
    email: str
    telegram_id: int
    password: str
    registered_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def to_read_schema(self) -> UserReadSchema:
        return UserReadSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            telegram_id=self.telegram_id,
        )

    def to_detail_read_schema(self) -> UserDetailReadSchema:
        return UserDetailReadSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            telegram_id=self.telegram_id,
            registered_at=self.registered_at,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
        )
