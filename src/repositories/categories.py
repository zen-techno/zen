from src.core.repository import SQLAlchemyRepository
from src.models import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category
