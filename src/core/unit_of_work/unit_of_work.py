from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.repositories import (
        CategoryRepository,
        ExpenseRepository,
        UserRepository,
    )


class AbstractUnitOfWork(ABC):
    users: UserRepository
    categories: CategoryRepository
    expenses: ExpenseRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    @abstractmethod
    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
