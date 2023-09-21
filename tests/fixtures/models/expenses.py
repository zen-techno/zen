from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Category, Expense, User

test_expenses: list[dict[str, Any]] = [
    {
        "id": UUID("7c1d7bf1-3977-4fae-a42d-c8504410b721"),
        "name": "Cafe near the sea",
        "amount": 500,
        "transaction_date": datetime(year=2023, month=9, day=15),
        "who_paid_id": UUID("b781d250c979470eb3aadbee25e681bd"),
        "category_id": UUID("7d9e924e-bf73-4389-9c84-146c7b1e7230"),
    },
    {
        "id": UUID("e8fad41a-30ca-4c9f-8b2f-be22b0c03999"),
        "name": "Products for Alice",
        "amount": 500,
        "transaction_date": datetime(year=2023, month=9, day=14),
        "who_paid_id": UUID("58d69d5e392e442999ace2b19efdf155"),
        "category_id": UUID("7d9e924e-bf73-4389-9c84-146c7b1e7230"),
    },
]


@pytest.fixture()
async def create_expenses_fixture(
    create_users_fixture: list[User],
    create_categories_fixture: list[Category],
    database_session: AsyncSession,
) -> list[Expense]:
    query = (
        insert(Expense)
        .values(test_expenses)
        .returning(Expense)
        .options(selectinload(Expense.who_paid))
        .options(selectinload(Expense.category))
    )
    result = await database_session.execute(query)
    result = result.scalars().all()
    await database_session.commit()

    return list(result)
