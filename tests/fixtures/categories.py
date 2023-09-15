from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category


@pytest.fixture()
async def create_categories(database_session: AsyncSession) -> list[Category]:
    categories = [
        Category(
            id=UUID("7d9e924e-bf73-4389-9c84-146c7b1e7230"),
            name="Coffee",
        ),
        Category(
            id=UUID("968b204f-eca7-4a8c-a04e-c0b5523b6eeb"),
            name="Products",
        ),
    ]
    database_session.add_all(categories)
    await database_session.commit()
    return categories
