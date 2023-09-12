from backend.src.core.repository import SQLAlchemyRepository
from backend.src.models import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category
