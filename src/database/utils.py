import asyncio

from fastapi.logger import logger
from sqlalchemy import text

from src.database.database import async_session_maker
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def check_database_connection() -> None:
    try:
        async with async_session_maker() as session:
            session: AsyncSession
            await session.execute(text("SELECT 1"))
    except ConnectionRefusedError:
        logger.error(
            "ERROR: \t  Couldn't connect to the database. Retry after 5 seconds"
        )
        await asyncio.sleep(5)
        await check_database_connection()
