from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload

from src.core.repository import SQLAlchemyRepository
from src.core.repository.exceptions import RepositoryError, RepositoryIntegrityError
from src.core.repository.repository import ID, EntityDict, EntityReadSchema
from src.models import Expense


class ExpenseRepository(SQLAlchemyRepository):
    model = Expense

    async def get_all(self) -> list[EntityReadSchema]:
        async with self.session_maker() as session:
            query = (
                select(self.model)
                .options(selectinload(self.model.who_paid))
                .options(selectinload(self.model.category))
            )
            try:
                result = await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                raise RepositoryError() from exc

            return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by: Any) -> EntityReadSchema | None:
        async with self.session_maker() as session:
            query = (
                select(self.model)
                .filter_by(**filter_by)
                .options(selectinload(self.model.who_paid))
                .options(selectinload(self.model.category))
            )
            try:
                result = await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                raise RepositoryError() from exc

            if result := result.scalar_one_or_none():
                return result.to_read_model()
            return None

    async def add_one(self, *, data: EntityDict) -> EntityReadSchema:
        async with self.session_maker() as session:
            query = (
                insert(self.model)
                .values(**data)
                .returning(self.model)
                .options(selectinload(self.model.who_paid))
                .options(selectinload(self.model.category))
            )
            try:
                result = await session.execute(query)
                await session.commit()
            except IntegrityError as exc:
                await session.rollback()
                raise RepositoryIntegrityError() from exc
            except SQLAlchemyError as exc:
                await session.rollback()
                raise RepositoryError() from exc

            return result.scalar_one().to_read_model()

    async def update_one(self, *, id: ID, data: EntityDict) -> EntityReadSchema:
        async with self.session_maker() as session:
            query = (
                update(self.model)
                .values(**data)
                .filter_by(id=id)
                .returning(self.model)
                .options(selectinload(self.model.who_paid))
                .options(selectinload(self.model.category))
            )
            try:
                result = await session.execute(query)
                await session.commit()
            except IntegrityError as exc:
                await session.rollback()
                raise RepositoryIntegrityError() from exc
            except SQLAlchemyError as exc:
                await session.rollback()
                raise RepositoryError() from exc

            return result.scalar_one().to_read_model()
