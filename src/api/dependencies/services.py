from typing import Annotated

from fastapi import Depends

from src.repositories import (
    CategoryRepository,
    ExpenseRepository,
    UserRepository,
)
from src.services import CategoryService, ExpenseService, UserService


def get_user_service() -> UserService:
    return UserService(UserRepository)


def get_category_service() -> CategoryService:
    return CategoryService(CategoryRepository)


def get_expense_service() -> ExpenseService:
    return ExpenseService(ExpenseRepository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]
CategoryServiceDepends = Annotated[
    CategoryService, Depends(get_category_service)
]
ExpenseServiceDepends = Annotated[ExpenseService, Depends(get_expense_service)]
