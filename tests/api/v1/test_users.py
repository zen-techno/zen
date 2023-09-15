from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class TestUserAPI:
    async def test_get_all_users_empty(self, aclient: AsyncClient) -> None:
        response = await aclient.get("api/v1/users")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == []

    async def test_get_all_users(
        self, aclient: AsyncClient, create_users: list[User]
    ) -> None:
        response = await aclient.get("api/v1/users")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2
        assert body == jsonable_encoder(
            [u.to_read_model() for u in create_users]
        )

    async def test_get_one_user(
        self, aclient: AsyncClient, create_users: list[User]
    ) -> None:
        response = await aclient.get(
            "api/v1/users/b781d250-c979-470e-b3aa-dbee25e681bd"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 3, "Incorrect amount of fields"
        assert body.get("id") == "b781d250-c979-470e-b3aa-dbee25e681bd"
        assert body.get("name") == "Alice"
        assert body.get("telegram_id") == 1

    async def test_user_not_found(
        self, aclient: AsyncClient, create_users: list[User]
    ) -> None:
        response = await aclient.get(
            "api/v1/users/b781d250-ffff-ffff-ffff-dbee25e681bd"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == {"detail": "User is not found"}

    async def test_create_user(
        self, aclient: AsyncClient, database_session: AsyncSession
    ) -> None:
        response = await aclient.post(
            "api/v1/users",
            json={"name": "Robert", "telegram_id": 10},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        user_id = body.get("id")
        user_name = body.get("name")
        user_telegram_id = body.get("telegram_id")

        assert len(body) == 3
        assert user_id
        assert user_name == "Robert"
        assert user_telegram_id == 10

        query = select(User).filter_by(id=user_id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert user_id == str(result.id)
        assert user_name == result.name
        assert user_telegram_id == result.telegram_id

    async def test_update_user(
        self,
        aclient: AsyncClient,
        create_users: list[User],
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.put(
            "api/v1/users/b781d250-c979-470e-b3aa-dbee25e681bd",
            json={"name": "Al", "telegram_id": 12},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        user_id = body.get("id")
        user_name = body.get("name")
        user_telegram_id = body.get("telegram_id")

        assert len(body) == 3
        assert user_id == "b781d250-c979-470e-b3aa-dbee25e681bd"
        assert user_name == "Al"
        assert user_telegram_id == 12

        query = (
            select(User)
            .filter_by(id=user_id)
            .execution_options(populate_existing=True)
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert user_id == str(result.id)
        assert user_name == result.name
        assert user_telegram_id == result.telegram_id

    async def test_delete_user(
        self,
        aclient: AsyncClient,
        create_users: list[User],
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.delete(
            "api/v1/users/b781d250-c979-470e-b3aa-dbee25e681bd",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(User).filter_by(
            id="b781d250-c979-470e-b3aa-dbee25e681bd"
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None
