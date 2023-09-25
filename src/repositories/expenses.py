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
        async with self.session_maker() as session:
            query = (
                select(self.model)
                .options(selectinload(self.model.who_paid))
                .options(selectinload(self.model.category))
            )
            try:
                result = await session.execute(query)
            except (SQLAlchemyError, Exception) as exc:
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
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc

            if result := result.scalars().first():
                return result.to_read_model()
            return None

    async def add_one(self, *, data: EntityDict) -> EntityReadSchema:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    existence_user_query = select(
                        self.model.who_paid.id
                    ).filter_by(id=data["who_paid_id"])
                    result = await session.execute(existence_user_query)
                    user_is_exist = result.scalar_one_or_none()
                    if not user_is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    existence_category_query = select(
                        self.model.category.id
                    ).filter_by(id=data["category_id"])
                    result = await session.execute(existence_category_query)
                    category_is_exist = result.scalar_one_or_none()
                    if not category_is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    add_query = (
                        insert(self.model)
                        .values(**data)
                        .returning(self.model)
                        .options(selectinload(self.model.who_paid))
                        .options(selectinload(self.model.category))
                    )
                    result = await session.execute(add_query)
                    await session.commit()

                except IntegrityError as exc:
                    await session.rollback()
                    raise RepositoryIntegrityError() from exc
                except (SQLAlchemyError, Exception) as exc:
                    await session.rollback()
                    raise RepositoryError() from exc

                return result.scalar_one().to_read_model()

    async def update_one(self, *, id: ID, data: EntityDict) -> EntityReadSchema:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    existence_user_query = select(
                        self.model.who_paid
                    ).filter_by(id=data["who_paid_id"])
                    result = await session.execute(existence_user_query)
                    user_is_exist = result.scalar_one_or_none()
                    if not user_is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    existence_category_query = select(
                        self.model.category
                    ).filter_by(id=data["category_id"])
                    result = await session.execute(existence_category_query)
                    category_is_exist = result.scalar_one_or_none()
                    if not category_is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    query = (
                        update(self.model)
                        .values(**data)
                        .filter_by(id=id)
                        .returning(self.model)
                        .options(selectinload(self.model.who_paid))
                        .options(selectinload(self.model.category))
                    )

                    result = await session.execute(query)
                    await session.commit()

                except IntegrityError as exc:
                    await session.rollback()
                    raise RepositoryIntegrityError() from exc
                except (SQLAlchemyError, Exception) as exc:
                    await session.rollback()
                    raise RepositoryError() from exc

                return result.scalar_one().to_read_model()
