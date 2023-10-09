from typing import Any

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ExpenseModel, UserModel
from tests.fixtures.models import test_users

API_PATH = "api/v1"


class TestUserAPI:
    async def test_get_all_users_empty(self, aclient: AsyncClient) -> None:
        response = await aclient.get(f"{API_PATH}/users")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"
        assert response.json() == []

    async def test_get_all_users(
        self, aclient: AsyncClient, create_users_fixture: list[UserModel]
    ) -> None:
        response = await aclient.get(f"{API_PATH}/users")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == len(create_users_fixture)

        assert body == jsonable_encoder(
            [u.to_dataclass() for u in create_users_fixture]
        )

    @pytest.mark.parametrize("user", test_users)
    async def test_get_one_user(
        self,
        user: dict[str, Any],
        aclient: AsyncClient,
        create_users_fixture: list[UserModel],
    ) -> None:
        user_uuid = str(user["id"])
        response = await aclient.get(f"{API_PATH}/users/{user_uuid}")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 3

        assert body["id"] == user_uuid
        assert body["name"] == user["name"]
        assert body["telegram_id"] == user["telegram_id"]

    async def test_user_not_found(
        self, aclient: AsyncClient, create_users_fixture: list[UserModel]
    ) -> None:
        user_uuid = "b781d250-ffff-ffff-ffff-dbee25e681bd"
        response = await aclient.get(f"{API_PATH}/users/{user_uuid}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"detail": "User is not found"}

    @pytest.mark.parametrize("user", test_users)
    async def test_create_user(
        self,
        user: dict[str, Any],
        aclient: AsyncClient,
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.post(
            f"{API_PATH}/users",
            json={"name": user["name"], "telegram_id": user["telegram_id"]},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 3

        created_user_id = body["id"]
        created_user_name = body["name"]
        created_user_telegram_id = body["telegram_id"]

        assert created_user_id
        assert created_user_name == user["name"]
        assert created_user_telegram_id == user["telegram_id"]

        query = select(UserModel).filter_by(id=created_user_id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert created_user_id == str(result.id)
        assert created_user_name == result.name
        assert created_user_telegram_id == result.telegram_id

    @pytest.mark.parametrize("user", test_users)
    async def test_update_user(
        self,
        user: dict[str, Any],
        aclient: AsyncClient,
        create_users_fixture: list[UserModel],
        database_session: AsyncSession,
    ) -> None:
        user_uuid = str(user["id"])
        expected_name_update = "Al"
        expected_telegram_id_update = 12

        response = await aclient.put(
            f"{API_PATH}/users/{user_uuid}",
            json={
                "name": expected_name_update,
                "telegram_id": expected_telegram_id_update,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"

        body = response.json()
        assert len(body) == 3

        updated_user_id = body["id"]
        updated_user_name = body["name"]
        updated_user_telegram_id = body["telegram_id"]

        assert updated_user_id == user_uuid
        assert updated_user_name == expected_name_update
        assert updated_user_telegram_id == expected_telegram_id_update

        query = (
            select(UserModel)
            .filter_by(id=updated_user_id)
            .execution_options(populate_existing=True)
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert updated_user_id == str(result.id)
        assert updated_user_name == result.name
        assert updated_user_telegram_id == result.telegram_id

    @pytest.mark.parametrize("user", test_users)
    async def test_delete_user(
        self,
        user: dict[str, Any],
        aclient: AsyncClient,
        create_expenses_fixture: list[ExpenseModel],
        database_session: AsyncSession,
    ) -> None:
        user_uuid = str(user["id"])
        response = await aclient.delete(
            f"{API_PATH}/users/{user_uuid}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(UserModel).filter_by(id=user_uuid)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None

        query = select(ExpenseModel).filter_by(who_paid_id=user_uuid)
        result = await database_session.execute(query)
        result = list(result.scalars().all())

        assert not result
