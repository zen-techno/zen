from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import SQLAlchemyRepository
from tests.fixtures.database.database_metadata import Entity, EntityReadSchema
from tests.fixtures.models import test_entities


class TestSQLAlchemyRepository:
    async def test_get_all(
        self,
        repository: SQLAlchemyRepository,
        create_entities_fixture: list[Entity],
    ) -> None:
        entities = await repository.get_all()

        assert len(entities) == len(create_entities_fixture)

        for entity in entities:
            assert isinstance(entity, EntityReadSchema)

        assert [e.model_dump() for e in entities] == test_entities

    async def test_get_all_empty(
        self, repository: SQLAlchemyRepository
    ) -> None:
        entities = await repository.get_all()

        assert len(entities) == 0
        assert entities == []

    @pytest.mark.parametrize("entity", test_entities)
    async def test_get_one_by_id(
        self,
        entity: dict[str, Any],
        repository: SQLAlchemyRepository,
        create_entities_fixture: list[Entity],
    ) -> None:
        database_entity = await repository.get_one(id=entity["id"])

        assert database_entity is not None
        assert isinstance(database_entity, EntityReadSchema)
        assert database_entity.model_dump() == entity

    async def test_get_one_by_many_param(
        self,
        repository: SQLAlchemyRepository,
        create_entities_fixture: list[Entity],
    ) -> None:
        params = {
            "username": test_entities[0]["username"],
            "balance": test_entities[0]["balance"],
        }
        database_entity = await repository.get_one(**params)

        assert database_entity is not None
        assert isinstance(database_entity, EntityReadSchema)
        assert database_entity.model_dump() == test_entities[0]

    async def test_get_one_not_found(
        self,
        repository: SQLAlchemyRepository,
        create_entities_fixture: list[Entity],
    ) -> None:
        params = {
            "username": "JackJack",
        }
        database_entity = await repository.get_one(**params)
        assert database_entity is None

    @pytest.mark.parametrize("entity", test_entities)
    async def test_add_one(
        self,
        entity: dict[str, Any],
        repository: SQLAlchemyRepository,
        database_session: AsyncSession,
    ) -> None:
        created_entity = await repository.add_one(
            data={"username": entity["username"], "balance": entity["balance"]}
        )
        assert created_entity is not None
        assert isinstance(created_entity, EntityReadSchema)

        assert created_entity.id
        assert created_entity.username == entity["username"]
        assert created_entity.balance == entity["balance"]

        query = select(Entity).filter_by(id=created_entity.id)
        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result.to_read_model() == created_entity

    async def test_add_one_unique(
        self,
        repository: SQLAlchemyRepository,
    ) -> None:
        ...

    @pytest.mark.parametrize("entity", test_entities)
    async def test_update_one(
        self,
        entity: dict[str, Any],
        repository: SQLAlchemyRepository,
        database_session: AsyncSession,
        create_entities_fixture: list[Entity],
    ) -> None:
        new_balance = 0
        updated_entity = await repository.update_one(
            id=entity["id"], data={"balance": new_balance}
        )
        assert updated_entity is not None
        assert isinstance(updated_entity, EntityReadSchema)

        assert updated_entity.id == entity["id"]
        assert updated_entity.username == entity["username"]
        assert updated_entity.balance == new_balance

        query = (
            select(Entity)
            .filter_by(id=entity["id"])
            .execution_options(populate_existing=True)
        )

        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result.to_read_model() == updated_entity

    async def test_update_or_unique(
        self,
        repository: SQLAlchemyRepository,
    ) -> None:
        ...

    @pytest.mark.parametrize("entity", test_entities)
    async def test_delete_one(
        self,
        entity: dict[str, Any],
        repository: SQLAlchemyRepository,
        database_session: AsyncSession,
        create_users_fixture: list[Entity],
    ) -> None:
        await repository.delete_one(id=entity["id"])

        query = select(Entity).filter_by(id=entity["id"])

        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None
