from typing import Any
from uuid import UUID

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel

test_users: list[dict[str, Any]] = [
    {
        "id": UUID("b781d250c979470eb3aadbee25e681bd"),
        "name": "Alice",
        "telegram_id": 1,
    },
    {
        "id": UUID("58d69d5e392e442999ace2b19efdf155"),
        "name": "Bob",
        "telegram_id": 2,
    },
]


@pytest.fixture()
async def create_users_fixture(
    database_session: AsyncSession,
) -> list[UserModel]:
    query = insert(UserModel).values(test_users).returning(UserModel)

    result = await database_session.execute(query)
    result = result.scalars().all()
    await database_session.commit()

    return list(result)
