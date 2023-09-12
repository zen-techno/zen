from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

engine = create_async_engine(url=settings.database.dsn, echo=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base: DeclarativeBase = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_maker() as session:
        yield session
