import asyncio
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from fastapi.logger import logger
from passlib.context import CryptContext
from sqlalchemy import select, text

from src.models.users import UserModel
from src.settings import settings
from src.storage.sqlalchemy.database import async_session_maker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

pwd_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


async def create_superuser() -> None:
    try:
        async with async_session_maker() as session:
            session: AsyncSession
            query = select(UserModel).filter_by(
                email=settings.auth.superuser_email
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result is not None:
                return

            superuser = UserModel(
                id=uuid4(),
                name="Admin",
                email=settings.auth.superuser_email,
                telegram_id=1,
                password=pwd_crypt_context.hash(
                    settings.auth.superuser_password.get_secret_value()
                ),
                registered_at=datetime.utcnow(),
                is_active=True,
                is_superuser=True,
                is_verified=True,
            )
            session.add(superuser)
            await session.commit()
            logger.info(
                f"INFO: \t  Superuser {settings.auth.superuser_email} created"
            )
    except Exception as exc:
        logger.exception(exc)
        return
