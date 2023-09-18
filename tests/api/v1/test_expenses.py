from typing import Any

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fixtures.expenses import test_expenses
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category, Expense, User

API_PATH = "api/v1"


class TestExpenseAPI:
    async def test_get_all_expenses_empty(self, aclient: AsyncClient) -> None:
        response = await aclient.get(f"{API_PATH}/expenses")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"
        assert response.json() == []

    async def test_get_all_expenses(
        self, aclient: AsyncClient, create_expenses_fixture: list[Expense]
    ) -> None:
        response = await aclient.get(f"{API_PATH}/expenses")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 2

        assert body == jsonable_encoder(
            [e.to_read_model() for e in create_expenses_fixture]
        )

    @pytest.mark.parametrize("expense", test_expenses)
    async def test_get_one_expense(
        self,
        expense: dict[str, Any],
        aclient: AsyncClient,
        create_expenses_fixture: list[Expense],
    ) -> None:
        expense_uuid = str(expense["id"])
        response = await aclient.get(f"{API_PATH}/expenses/{expense_uuid}")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 6

        assert body["id"] == expense_uuid
        assert body["name"] == expense["name"]
        assert body["amount"] == expense["amount"]
        assert body["transaction_date"] == jsonable_encoder(
            expense["transaction_date"]
        )
        assert body["who_paid"]["id"] == str(expense["who_paid_id"])
        assert body["category"]["id"] == str(expense["category_id"])

    async def test_expense_not_found(
        self, aclient: AsyncClient, create_expenses_fixture: list[Expense]
    ) -> None:
        expense_uuid = "b781d250-ffff-ffff-ffff-dbee25e681bd"
        response = await aclient.get(f"{API_PATH}/expenses/{expense_uuid}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"detail": "Expense is not found"}

    @pytest.mark.parametrize("expense", test_expenses)
    async def test_create_expense(
        self,
        expense: dict[str, Any],
        aclient: AsyncClient,
        database_session: AsyncSession,
        create_users_fixture: list[User],
        create_categories_fixture: list[Category],
    ) -> None:
        response = await aclient.post(
            f"{API_PATH}/expenses",
            json={
                "name": expense["name"],
                "amount": expense["amount"],
                "who_paid_id": str(expense["who_paid_id"]),
                "category_id": str(expense["category_id"]),
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 6

        created_expense_id = body["id"]
        created_transaction_date = body["transaction_date"]
        created_expense_name = body["name"]
        created_expense_amount = body["amount"]
        created_who_paid_id = body["who_paid"]["id"]
        created_category_id = body["category"]["id"]

        assert created_expense_id
        assert created_transaction_date
        assert created_expense_name == expense["name"]
        assert created_expense_amount == expense["amount"]
        assert created_who_paid_id == str(expense["who_paid_id"])
        assert created_category_id == str(expense["category_id"])

        query = select(Expense).filter_by(id=created_expense_id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert created_expense_id == str(result.id)
        assert created_transaction_date == jsonable_encoder(
            result.transaction_date
        )
        assert created_expense_name == result.name
        assert created_expense_amount == result.amount
        assert created_who_paid_id == str(result.who_paid_id)
        assert created_category_id == str(result.category_id)

    @pytest.mark.parametrize("expense", test_expenses)
    async def test_update_expense(
        self,
        expense: dict[str, Any],
        aclient: AsyncClient,
        create_expenses_fixture: list[Expense],
        database_session: AsyncSession,
    ) -> None:
        expense_uuid = str(expense["id"])
        expected_name_update = "Beer"
        expected_amount_update = 100

        response = await aclient.put(
            f"{API_PATH}/expenses/{expense_uuid}",
            json={
                "name": expected_name_update,
                "amount": expected_amount_update,
                "who_paid_id": str(expense["who_paid_id"]),
                "category_id": str(expense["category_id"]),
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 6

        updated_expense_id = body["id"]
        updated_transaction_date = body["transaction_date"]
        updated_expense_name = body["name"]
        updated_expense_amount = body["amount"]
        updated_who_paid_id = body["who_paid"]["id"]
        updated_category_id = body["category"]["id"]

        assert updated_transaction_date == jsonable_encoder(
            expense["transaction_date"]
        )
        assert updated_expense_id == expense_uuid
        assert updated_expense_name == expected_name_update
        assert updated_expense_amount == expected_amount_update
        assert updated_who_paid_id == str(expense["who_paid_id"])
        assert updated_category_id == str(expense["category_id"])

        query = (
            select(Expense)
            .filter_by(id=updated_expense_id)
            .execution_options(populate_existing=True)
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert updated_expense_id == str(result.id)
        assert updated_transaction_date == jsonable_encoder(
            result.transaction_date
        )
        assert updated_expense_name == result.name
        assert updated_expense_amount == result.amount
        assert updated_who_paid_id == str(result.who_paid_id)
        assert updated_category_id == str(result.category_id)

    @pytest.mark.parametrize("expense", test_expenses)
    async def test_delete_expense(
        self,
        expense: dict[str, Any],
        aclient: AsyncClient,
        create_expenses_fixture: list[Expense],
        database_session: AsyncSession,
    ) -> None:
        expense_uuid = str(expense["id"])
        response = await aclient.delete(
            f"{API_PATH}/expenses/{expense_uuid}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(Expense).filter_by(id=expense_uuid)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None
