from src.core.repository import SQLAlchemyRepository
from src.models import Expense


class ExpenseRepository(SQLAlchemyRepository):
    model = Expense
