from src.core.repository import SQLAlchemyRepository
from src.models import CategoryModel


class CategoryRepository(SQLAlchemyRepository):
    model = CategoryModel
