from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, **filter_by: Any) -> list[EntityReadSchema]:
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
        except (SQLAlchemyError, Exception) as exc:
            await self.session.rollback()
            raise RepositoryError() from exc

        return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by: Any) -> EntityReadSchema | None:
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
        except (SQLAlchemyError, Exception) as exc:
            await self.session.rollback()
            raise RepositoryError() from exc

        if result := result.scalars().first():
            return result.to_read_model()
        return None

    async def add_one(self, *, data: EntityDict) -> EntityReadSchema:
        query = insert(self.model).values(**data).returning(self.model)
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

    async def delete_one(self, *, id: ID) -> None:
        async with self.session.begin_nested():
            try:
                existence_query = select(self.model.id).filter_by(id=id)
                result = await self.session.execute(existence_query)
                is_exist = result.scalar_one_or_none()
                if not is_exist:
                    await self.session.rollback()
                    raise RepositoryDoesNotExistError()

                delete_query = delete(self.model).filter_by(id=id)
                await self.session.execute(delete_query)

            except (SQLAlchemyError, Exception) as exc:
                await self.session.rollback()
                raise RepositoryError() from exc
