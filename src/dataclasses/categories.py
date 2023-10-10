from dataclasses import dataclass
from uuid import UUID

from src.schemas.categories import CategoryReadSchema


@dataclass(frozen=True, slots=True)
class Category:
    id: UUID
    name: str
    user_id: UUID

    def to_read_schema(self) -> CategoryReadSchema:
        return CategoryReadSchema(
            id=self.id, name=self.name, user_id=self.user_id
        )
