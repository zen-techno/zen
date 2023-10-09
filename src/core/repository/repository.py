from abc import ABC, abstractmethod
from typing import Any, TypeAlias, Union
from uuid import UUID

ID: TypeAlias = Union[UUID, int, str]
EntityDict: TypeAlias = dict[str, Any]
Entity: TypeAlias = Any


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Entity]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by: Any) -> Entity | None:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, *, data: EntityDict) -> Entity:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *, id: ID, data: EntityDict) -> Entity:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *, id: ID) -> None:
        raise NotImplementedError
