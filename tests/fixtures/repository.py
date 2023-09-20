import pytest
from fixtures.database.database_metadata import Entity

from src.core.repository import SQLAlchemyRepository


@pytest.fixture()
def repository() -> SQLAlchemyRepository:
    repo = SQLAlchemyRepository()
    repo.model = Entity
    return repo
