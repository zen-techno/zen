import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.database import async_session_maker, engine
from src.main import app
from src.models import Base
from src.settings import settings

Base: DeclarativeBase


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
async def prepare_database(check_database_mode) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="function")
async def clear_database_tables(
    database_session: AsyncSession,
) -> AsyncGenerator[None, AsyncSession]:
    yield
    try:
        for table in reversed(Base.metadata.sorted_tables):
            await database_session.execute(table.delete())
        await database_session.commit()
    except Exception:
        pass


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
async def aclient() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as aclient:
        yield aclient
