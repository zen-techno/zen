from abc import ABC, abstractmethod
from typing import Any, TypeAlias, Union
from uuid import UUID

from pydantic import BaseModel

ID: TypeAlias = Union[UUID, int, str]
EntityDict: TypeAlias = dict[str, Any]
EntityReadSchema: TypeAlias = Union[BaseModel, Any]


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[EntityReadSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by: Any) -> EntityReadSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, *, data: EntityDict) -> EntityReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *, id: ID, data: EntityDict) -> EntityReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *, id: ID) -> None:
        raise NotImplementedError
