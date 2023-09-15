from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


@pytest.fixture()
async def create_users(database_session: AsyncSession) -> list[User]:
    users = [
        User(
            id=UUID("b781d250c979470eb3aadbee25e681bd"),
            name="Alice",
            telegram_id=1,
        ),
        User(
            id=UUID("58d69d5e392e442999ace2b19efdf155"),
            name="Bob",
            telegram_id=2,
        ),
    ]
    database_session.add_all(users)
    await database_session.commit()
    return users
