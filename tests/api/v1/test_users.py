import pytest
from fastapi import status
from httpx import AsyncClient

# @pytest.fixture()
# async def create_users():
#     ...


class TestUserAPI:
    async def test_get_all_users_empty(self, aclient: AsyncClient):
        response = await aclient.get("api/v1/users")

        assert response.status_code == status.HTTP_200_OK, "Invalid status code"
        assert response.json() == [], "Invalid json response body"

    # async def test_get_all_users(self, aclient):
    #     ...
