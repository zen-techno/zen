from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.core.unit_of_work.unit_of_work import AbstractUnitOfWork
from src.repositories import (
    CategoryRepository,
    ExpenseRepository,
    UserRepository,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable) -> None:
        self.session_factory = session_factory

    async def __aenter__(self, *args: Any) -> UnitOfWork:
        self.session: AsyncSession = self.session_factory()

        self.users = UserRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.expenses = ExpenseRepository(self.session)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
