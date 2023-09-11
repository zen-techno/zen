from backend.src.core.repository import SQLAlchemyRepository
from backend.src.models import Expense


class ExpenseRepository(SQLAlchemyRepository):
    model = Expense
