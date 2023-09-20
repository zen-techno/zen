from collections.abc import AsyncGenerator

import pytest
from fixtures.database.database_metadata import TestBase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker, engine
from src.settings import settings


@pytest.fixture()
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def check_database_mode() -> AsyncGenerator[None, None]:
    assert settings.database.mode == "test" and (
        "test" in settings.database.database_name
    ), "Invalid .env file. You need to create .test.env"
    yield


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(
    check_database_mode: AsyncGenerator[None, None]
) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)


@pytest.fixture(autouse=True, scope="function")
async def clear_database_tables(
    database_session: AsyncSession,
) -> AsyncGenerator[None, AsyncSession]:
    yield
    try:
        for table in reversed(TestBase.metadata.sorted_tables):
            await database_session.execute(table.delete())
        await database_session.commit()
    except Exception:
        pass
