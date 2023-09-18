from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_read_model(self) -> BaseModel:
        raise NotImplementedError
