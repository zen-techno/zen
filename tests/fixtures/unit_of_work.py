from typing import TYPE_CHECKING, Any

import pytest

from src.core.repository import SQLAlchemyRepository
from src.core.unit_of_work import UnitOfWork
from src.repositories import (
    CategoryRepository,
    ExpenseRepository,
    UserRepository,
)
from src.storage.sqlalchemy import async_session_maker
from tests.fixtures.database.database_metadata import EntityModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class EntityRepository(SQLAlchemyRepository):
    model = EntityModel


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
