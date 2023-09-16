from typing import Any

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category
from tests.fixtures.categories import test_categories


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

    @pytest.mark.parametrize("category", test_categories)
    async def test_get_one_category(
        self,
        category: dict[str, Any],
        aclient: AsyncClient,
        create_categories_fixture: list[Category],
    ) -> None:
        category_uuid = str(category["id"])
        response = await aclient.get(f"api/v1/categories/{category_uuid}")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2
        assert body.get("id") == category_uuid
        assert body.get("name") == category["name"]

    async def test_category_not_found(
        self, aclient: AsyncClient, create_categories_fixture: list[Category]
    ) -> None:
        category_uuid = "b781d250-ffff-ffff-ffff-dbee25e681bd"
        response = await aclient.get(f"api/v1/categories/{category_uuid}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == {"detail": "Category is not found"}

    @pytest.mark.parametrize("category", test_categories)
    async def test_create_category(
        self,
        category: dict[str, Any],
        aclient: AsyncClient,
        database_session: AsyncSession,
    ) -> None:
        response = await aclient.post(
            "api/v1/categories",
            json={"name": category["name"]},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2

        created_category_id = body.get("id")
        created_category_name = body.get("name")

        assert created_category_id
        assert created_category_name == category["name"]

        query = select(Category).filter_by(id=created_category_id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert created_category_id == str(result.id)
        assert created_category_name == result.name

    @pytest.mark.parametrize("category", test_categories)
    async def test_update_category(
        self,
        category: dict[str, Any],
        aclient: AsyncClient,
        create_categories_fixture: list[Category],
        database_session: AsyncSession,
    ) -> None:
        category_uuid = str(category["id"])
        expected_name_update = "Dinner"

        response = await aclient.put(
            f"api/v1/categories/{category_uuid}",
            json={"name": expected_name_update},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers.get("content-type") == "application/json"

        body = response.json()
        assert len(body) == 2

        updated_category_id = body.get("id")
        updated_category_name = body.get("name")

        assert updated_category_id == category_uuid
        assert updated_category_name == expected_name_update

        query = (
            select(Category)
            .filter_by(id=updated_category_id)
            .execution_options(populate_existing=True)
        )
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result
        assert updated_category_id == str(result.id)
        assert updated_category_name == result.name

    @pytest.mark.parametrize("category", test_categories)
    async def test_delete_category(
        self,
        category: dict[str, Any],
        aclient: AsyncClient,
        create_categories_fixture: list[Category],
        database_session: AsyncSession,
    ) -> None:
        category_uuid = str(category["id"])
        response = await aclient.delete(
            f"api/v1/categories/{category_uuid}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(Category).filter_by(id=category_uuid)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None
