from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeAlias, Union
from uuid import UUID

from pydantic import BaseModel

ID: TypeAlias = Union[int, UUID, str]
DataDict: TypeAlias = Dict[str, Any]
ReadSchema: TypeAlias = Union[BaseModel, Any]


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *, data: DataDict) -> ReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[ReadSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by) -> Optional[ReadSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *, id: ID, data: DataDict) -> ReadSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *, id: ID) -> None:
        raise NotImplementedError
