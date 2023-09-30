from typing import TYPE_CHECKING, Any

import pytest

from src.core.repository import SQLAlchemyRepository
from src.core.unit_of_work import UnitOfWork
from src.database import async_session_maker
from src.repositories import (
    CategoryRepository,
    ExpenseRepository,
    UserRepository,
)
from tests.fixtures.database.database_metadata import Entity

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class EntityRepository(SQLAlchemyRepository):
    model = Entity


class UnitOfWorkForTest(UnitOfWork):
    async def __aenter__(self, *args: Any) -> UnitOfWork:
        self.session: AsyncSession = self.session_factory()

        self.users = UserRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.expenses = ExpenseRepository(self.session)
        self.entities = EntityRepository(self.session)
        return self


@pytest.fixture()
def uow() -> UnitOfWorkForTest:
    return UnitOfWorkForTest(session_factory=async_session_maker)
