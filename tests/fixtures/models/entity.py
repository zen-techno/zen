from typing import Any
from uuid import UUID

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.database.database_metadata import Entity

test_entities: list[dict[str, Any]] = [
    {
        "id": UUID("4be2bb60-8d51-4a6b-8ef6-12e98d5ab905"),
        "username": "Qwerty",
        "balance": 100,
    },
    {
        "id": UUID("b49cdfca-2c19-4fde-afb2-6d33021ffc67"),
        "username": "Admin",
        "balance": 0,
    },
    {
        "id": UUID("c49f77c1-bc4a-4156-b479-6e0e055e9b72"),
        "username": "Bad Bob",
        "balance": 0,
    },
]


@pytest.fixture()
async def create_entities_fixture(
    database_session: AsyncSession,
) -> list[Entity]:
    query = insert(Entity).values(test_entities).returning(Entity)

    result = await database_session.execute(query)
    result = result.scalars().all()
    await database_session.commit()

    return list(result)
