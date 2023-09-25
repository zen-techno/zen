from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.repository.exceptions import (
    RepositoryDoesNotExistError,
    RepositoryError,
    RepositoryIntegrityError,
)
from src.core.repository.repository import (
    ID,
    AbstractRepository,
    EntityDict,
    EntityReadSchema,
)
from src.database.database import async_session_maker


class SQLAlchemyRepository(AbstractRepository):
    model = None
    session_maker = async_session_maker

    async def get_all(self) -> list[EntityReadSchema]:
        async with self.session_maker() as session:
            query = select(self.model)
            try:
                result = await session.execute(query)
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc

            return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by: Any) -> EntityReadSchema | None:
        async with self.session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
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
            query = insert(self.model).values(**data).returning(self.model)
            try:
                result = await session.execute(query)
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
                    existence_query = select(self.model.id).filter_by(id=id)
                    result = await session.execute(existence_query)
                    is_exist = result.scalar_one_or_none()
                    if not is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    update_query = (
                        update(self.model)
                        .values(**data)
                        .filter_by(id=id)
                        .returning(self.model)
                    )
                    result = await session.execute(update_query)
                    await session.commit()

                except IntegrityError as exc:
                    await session.rollback()
                    raise RepositoryIntegrityError() from exc
                except (SQLAlchemyError, Exception) as exc:
                    await session.rollback()
                    raise RepositoryError() from exc

                return result.scalar_one().to_read_model()

    async def delete_one(self, *, id: ID) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    existence_query = select(self.model.id).filter_by(id=id)
                    result = await session.execute(existence_query)
                    is_exist = result.scalar_one_or_none()
                    if not is_exist:
                        await session.rollback()
                        raise RepositoryDoesNotExistError()

                    delete_query = delete(self.model).filter_by(id=id)
                    await session.execute(delete_query)
                    await session.commit()
                except (SQLAlchemyError, Exception) as exc:
                    await session.rollback()
                    raise RepositoryError() from exc
