from abc import ABC, abstractmethod
from typing import Any, TypeAlias, Union
from uuid import UUID

from pydantic import BaseModel

ID: TypeAlias = Union[UUID, int, str]
DataDict: TypeAlias = dict[str, Any]
ReadSchema: TypeAlias = Union[BaseModel, Any]


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *, data: DataDict) -> ReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ReadSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by: Any) -> ReadSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *, id: ID, data: DataDict) -> ReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *, id: ID) -> None:
        raise NotImplementedError
