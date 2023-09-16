from uuid import UUID

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category


@pytest.fixture()
async def create_categories_fixture(
    database_session: AsyncSession,
) -> list[Category]:
    categories = [
        {"id": UUID("7d9e924e-bf73-4389-9c84-146c7b1e7230"), "name": "Coffee"},
        {
            "id": UUID("968b204f-eca7-4a8c-a04e-c0b5523b6eeb"),
            "name": "Products",
        },
    ]
    query = insert(Category).values(categories).returning(Category)

    result = await database_session.execute(query)
    result = result.scalars().all()
    await database_session.commit()

    return list(result)
