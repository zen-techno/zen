from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload

from src.core.repository import SQLAlchemyRepository
from src.core.repository.exceptions import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.core.repository.repository import ID, EntityDict, EntityReadSchema
from src.models import Expense


class ExpenseRepository(SQLAlchemyRepository):
    model = Expense

    async def get_all(self) -> list[EntityReadSchema]:
        query = (
            select(self.model)
            .options(selectinload(self.model.who_paid))
            .options(selectinload(self.model.category))
        )
        try:
            result = await self.session.execute(query)
        except (SQLAlchemyError, Exception) as exc:
            await self.session.rollback()
            raise RepositoryError() from exc

        return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by: Any) -> EntityReadSchema | None:
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(selectinload(self.model.who_paid))
            .options(selectinload(self.model.category))
        )
        try:
            result = await self.session.execute(query)
        except (SQLAlchemyError, Exception) as exc:
            await self.session.rollback()
            raise RepositoryError() from exc

        if result := result.scalars().first():
            return result.to_read_model()
        return None

    async def add_one(self, *, data: EntityDict) -> EntityReadSchema:
        query = (
            insert(self.model)
            .values(**data)
            .options(selectinload(self.model.who_paid))
            .options(selectinload(self.model.category))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(query)
        except IntegrityError as exc:
            await self.session.rollback()
            raise RepositoryIntegrityError() from exc
        except (SQLAlchemyError, Exception) as exc:
            await self.session.rollback()
            raise RepositoryError() from exc

        return result.scalar_one().to_read_model()

    async def update_one(self, *, id: ID, data: EntityDict) -> EntityReadSchema:
        async with self.session.begin_nested():
            try:
                existence_query = select(self.model.id).filter_by(id=id)
                result = await self.session.execute(existence_query)
                is_exist = result.scalar_one_or_none()
                if not is_exist:
                    await self.session.rollback()
                    raise RepositoryDoesNotExistError()

                update_query = (
                    update(self.model)
                    .values(**data)
                    .filter_by(id=id)
                    .options(selectinload(self.model.who_paid))
                    .options(selectinload(self.model.category))
                    .returning(self.model)
                )
                result = await self.session.execute(update_query)

            except IntegrityError as exc:
                await self.session.rollback()
                raise RepositoryIntegrityError() from exc
            except (SQLAlchemyError, Exception) as exc:
                await self.session.rollback()
                raise RepositoryError() from exc

            return result.scalar_one().to_read_model()
