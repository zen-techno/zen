import asyncio
from typing import TYPE_CHECKING

from fastapi.logger import logger
from sqlalchemy import text

from src.storage.sqlalchemy.database import async_session_maker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def check_database_connection() -> None:
    try:
        async with async_session_maker() as session:
            session: AsyncSession
            await session.execute(text("SELECT 1"))
    except ConnectionRefusedError:
        logger.error(
            "ERROR: \t  Couldn't connect to the sqlalchemy. Retry after 5 seconds"
        )
        await asyncio.sleep(5)
        await check_database_connection()
