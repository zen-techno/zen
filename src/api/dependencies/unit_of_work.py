from typing import Annotated

from fastapi import Depends

from src.core.unit_of_work import AbstractUnitOfWork, UnitOfWork
from src.storage.sqlalchemy import async_session_maker


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork(session_factory=async_session_maker)


UnitOfWorkDepends = Annotated[AbstractUnitOfWork, Depends(get_unit_of_work)]
