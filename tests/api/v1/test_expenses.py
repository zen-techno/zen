from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from src.models import Expense


class TestExpenseAPI:
    async def test_get_all_expenses_empty(self, aclient: AsyncClient) -> None:
        response = await aclient.get("api/v1/expenses")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == []

    async def test_get_all_expenses(
        self, aclient: AsyncClient, create_expenses_fixture: list[Expense]
    ) -> None:
        response = await aclient.get("api/v1/expenses")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2
        assert body == jsonable_encoder(
            [e.to_read_model() for e in create_expenses_fixture]
        )

    async def test_expense_not_found(
        self, aclient: AsyncClient, create_expenses_fixture: list[Expense]
    ) -> None:
        response = await aclient.get(
            "api/v1/expenses/b781d250-ffff-ffff-ffff-dbee25e681bd"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == {"detail": "Expense is not found"}

    # async def test_create_expense(
    #     self,
    #     aclient: AsyncClient,
    #     database_session: AsyncSession,
    #     create_expenses: list[Expense],
    # ) -> None:
    #     response = await aclient.post(
    #         "api/v1/expenses",
    #         json={
    #             "name": "Bob's Purchase",
    #             "amount": 1000,
    #             "who_paid_id": "58d69d5e-392e-4429-99ac-e2b19efdf155",
    #             "category_id": "968b204f-eca7-4a8c-a04e-c0b5523b6eeb",
    #         },
    #     )
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.headers.get("content-type") == "application/json"
    #
    #     body = response.json()
    #     expense_id = body.get("id")
    #     expense_name = body.get("name")
    #     transaction_date = body.get("transaction_date")
    #     who_paid = body.get("who_paid")
    #     category = body.get("category")
    #
    #     assert len(body) == 6
    #     assert expense_id
    #     assert transaction_date
    #     assert expense_name == "Bob's Purchase"
    #     assert who_paid.get("id") == "58d69d5e-392e-4429-99ac-e2b19efdf155"
    #     assert category.get("id") == "968b204f-eca7-4a8c-a04e-c0b5523b6eeb"
    #
    #     query = select(Expense).filter_by(id=expense_id)
    #     result = await database_session.execute(query)
    #     result = result.scalar_one_or_none()
    #
    #     assert result
    #     assert expense_id == str(result.id)
    #     assert expense_name == str(result.name)
    #     assert who_paid.get("id") == str(result.who_paid_id)
    #     assert category.get("id") == str(result.category_id)
    #
    #
    # async def test_invalid_data(self) -> None:
    #     raise NotImplementedError
