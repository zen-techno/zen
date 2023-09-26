from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker, engine
from src.settings import settings
from tests.fixtures.database.database_metadata import TestBase


@pytest.fixture()
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def _check_database_mode() -> None:
    assert (
        "test" in settings.database.database_name
    ), "Invalid .env file. You need to create .test.env"
    assert (
        settings.database.mode == "test"
    ), "Invalid .env file. You need to create .test.env"


@pytest.fixture(scope="session", autouse=True)
async def _prepare_database(
    _check_database_mode: None,
) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)


@pytest.fixture(autouse=True)
async def _clear_database_tables(
    database_session: AsyncSession,
) -> AsyncGenerator[None, AsyncSession]:
    yield
    try:
        for table in reversed(TestBase.metadata.sorted_tables):
            await database_session.execute(table.delete())
        await database_session.commit()
    except Exception:
        pass
