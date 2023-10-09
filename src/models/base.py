from abc import abstractmethod
from typing import Any

from sqlalchemy.orm import declarative_base

base = declarative_base()


class DeclarativeBase(base):
    __abstract__ = True

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_dataclass(self) -> Any:
        raise NotImplementedError
