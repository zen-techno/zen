from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.database.database_metadata import Entity, EntityReadSchema
from tests.fixtures.models import test_entities
from tests.fixtures.unit_of_work import UnitOfWorkForTest


class TestSQLAlchemyRepository:
    async def test_get_all(
        self,
        uow: UnitOfWorkForTest,
        create_entities_fixture: list[Entity],
    ) -> None:
        async with uow:
            entities = await uow.entities.get_all()

        assert len(entities) == len(create_entities_fixture)

        for entity in entities:
            assert isinstance(entity, EntityReadSchema)

        assert [e.model_dump() for e in entities] == test_entities

    async def test_get_all_empty(
        self,
        uow: UnitOfWorkForTest,
    ) -> None:
        async with uow:
            entities = await uow.entities.get_all()

        assert len(entities) == 0
        assert entities == []

    @pytest.mark.parametrize("entity", test_entities)
    async def test_get_one_by_id(
        self,
        entity: dict[str, Any],
        uow: UnitOfWorkForTest,
        create_entities_fixture: list[Entity],
    ) -> None:
        async with uow:
            database_entity = await uow.entities.get_one(id=entity["id"])

        assert database_entity is not None
        assert isinstance(database_entity, EntityReadSchema)
        assert database_entity.model_dump() == entity

    async def test_get_one_by_many_param(
        self,
        uow: UnitOfWorkForTest,
        create_entities_fixture: list[Entity],
    ) -> None:
        params = {
            "username": test_entities[0]["username"],
            "balance": test_entities[0]["balance"],
        }
        async with uow:
            database_entity = await uow.entities.get_one(**params)

        assert database_entity is not None
        assert isinstance(database_entity, EntityReadSchema)
        assert database_entity.model_dump() == test_entities[0]

    async def test_get_one_not_found(
        self,
        uow: UnitOfWorkForTest,
        create_entities_fixture: list[Entity],
    ) -> None:
        params = {
            "username": "JackJack",
        }
        async with uow:
            database_entity = await uow.entities.get_one(**params)
        assert database_entity is None

    @pytest.mark.parametrize("entity", test_entities)
    async def test_add_one(
        self,
        entity: dict[str, Any],
        uow: UnitOfWorkForTest,
        database_session: AsyncSession,
    ) -> None:
        async with uow:
            created_entity = await uow.entities.add_one(
                data={
                    "username": entity["username"],
                    "balance": entity["balance"],
                }
            )
            await uow.commit()
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
        uow: UnitOfWorkForTest,
    ) -> None:
        raise NotImplementedError

    @pytest.mark.parametrize("entity", test_entities)
    async def test_update_one(
        self,
        entity: dict[str, Any],
        uow: UnitOfWorkForTest,
        database_session: AsyncSession,
        create_entities_fixture: list[Entity],
    ) -> None:
        new_balance = 0
        async with uow:
            updated_entity = await uow.entities.update_one(
                id=entity["id"], data={"balance": new_balance}
            )
            await uow.commit()
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
        uow: UnitOfWorkForTest,
    ) -> None:
        raise NotImplementedError

    async def test_update_not_found(
        self,
        uow: UnitOfWorkForTest,
    ) -> None:
        raise NotImplementedError

    @pytest.mark.parametrize("entity", test_entities)
    async def test_delete_one(
        self,
        entity: dict[str, Any],
        uow: UnitOfWorkForTest,
        database_session: AsyncSession,
        create_entities_fixture: list[Entity],
    ) -> None:
        async with uow:
            await uow.entities.delete_one(id=entity["id"])
            await uow.commit()
        query = select(Entity).filter_by(id=entity["id"])

        result = await database_session.execute(query)
        result = result.scalar_one_or_none()

        assert result is None

    async def test_delete_not_found(
        self,
        uow: UnitOfWorkForTest,
    ) -> None:
        raise NotImplementedError
