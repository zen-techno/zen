from src.core.repository import SQLAlchemyRepository
from src.models import ExpenseModel


class ExpenseRepository(SQLAlchemyRepository):
    model = ExpenseModel
