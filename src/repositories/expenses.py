from typing import List, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload

from src.core.repository import SQLAlchemyRepository
from src.core.repository.repository import ID, DataDict, ReadSchema
from src.models import Expense


class ExpenseRepository(SQLAlchemyRepository):
    model = Expense

    async def add_one(self, *, data: DataDict) -> ReadSchema:
        async with self.session_maker() as session:
            query = (
                insert(self.model)
                .values(**data)
                .returning(self.model)
                .options(joinedload(self.model.who_paid))
                .options(joinedload(self.model.category))
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_read_model()

    async def get_all(self) -> List[ReadSchema]:
        async with self.session_maker() as session:
            query = (
                select(self.model)
                .options(joinedload(self.model.who_paid))
                .options(joinedload(self.model.category))
            )
            result = await session.execute(query)
            return [item.to_read_model() for item in result.scalars()]

    async def get_one(self, **filter_by) -> Optional[ReadSchema]:
        async with self.session_maker() as session:
            query = (
                select(self.model)
                .filter_by(**filter_by)
                .options(joinedload(self.model.who_paid))
                .options(joinedload(self.model.category))
            )
            result = await session.execute(query)
            if result := result.scalar_one_or_none():
                return result.to_read_model()
            return None

    async def update_one(self, *, id: ID, data: DataDict) -> ReadSchema:
        async with self.session_maker() as session:
            query = (
                update(self.model)
                .values(**data)
                .filter_by(id=id)
                .returning(self.model)
                .options(joinedload(self.model.who_paid))
                .options(joinedload(self.model.category))
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_read_model()
