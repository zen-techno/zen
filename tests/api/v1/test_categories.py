from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category


class TestCategoryAPI:
    async def test_get_all_categories_empty(self, aclient: AsyncClient) -> None:
        response = await aclient.get("api/v1/categories")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == []

    async def test_get_all_categories(
        self, aclient: AsyncClient, create_categories_fixture: list[Category]
    ) -> None:
        response = await aclient.get("api/v1/categories")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2
        assert body == jsonable_encoder(
            [c.to_read_model() for c in create_categories_fixture]
        )

    async def test_get_one_category(
        self, aclient: AsyncClient, create_categories_fixture: list[Category]
    ) -> None:
        response = await aclient.get(
            "api/v1/categories/7d9e924e-bf73-4389-9c84-146c7b1e7230"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2
        assert body.get("id") == "7d9e924e-bf73-4389-9c84-146c7b1e7230"
        assert body.get("name") == "Coffee"

    async def test_category_not_found(
        self, aclient: AsyncClient, create_categories_fixture: list[Category]
    ) -> None:
        response = await aclient.get(
            "api/v1/categories/b781d250-ffff-ffff-ffff-dbee25e681bd"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == {"detail": "Category is not found"}

    async def test_create_category(
        self, aclient: AsyncClient, database_session: AsyncSession
    ) -> None:
        response = await aclient.post(
            "api/v1/categories",
            json={"name": "Breakfast"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        category_id = body.get("id")
        category_name = body.get("name")

        assert len(body) == 2
        assert category_id
        assert category_name == "Breakfast"

        query = select(Category).filter_by(id=category_id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert category_id == str(result.id)
        assert category_name == result.name

    async def test_update_category(
        self,
        aclient: AsyncClient,
        create_categories_fixture: list[Category],
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.put(
            "api/v1/categories/7d9e924e-bf73-4389-9c84-146c7b1e7230",
            json={"name": "Dinner"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        category_id = body.get("id")
        category_name = body.get("name")

        assert len(body) == 2
        assert category_id == "7d9e924e-bf73-4389-9c84-146c7b1e7230"
        assert category_name == "Dinner"

        query = (
            select(Category)
            .filter_by(id=category_id)
            .execution_options(populate_existing=True)
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert category_id == str(result.id)
        assert category_name == result.name

    async def test_delete_category(
        self,
        aclient: AsyncClient,
        create_categories_fixture: list[Category],
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.delete(
            "api/v1/categories/7d9e924e-bf73-4389-9c84-146c7b1e7230",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(Category).filter_by(
            id="7d9e924e-bf73-4389-9c84-146c7b1e7230"
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None
