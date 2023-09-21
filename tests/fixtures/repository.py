import pytest

from src.core.repository import SQLAlchemyRepository
from tests.fixtures.database.database_metadata import Entity


@pytest.fixture()
def repository() -> SQLAlchemyRepository:
    repo = SQLAlchemyRepository()
    repo.model = Entity
    return repo
