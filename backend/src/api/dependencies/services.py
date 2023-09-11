from typing import Annotated

from fastapi import Depends

from backend.src.repositories import CategoryRepository, UserRepository
from backend.src.services import CategoryService, UserService


def get_user_service() -> UserService:
    return UserService(UserRepository)


def get_category_service() -> CategoryService:
    return CategoryService(CategoryRepository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]
CategoryServiceDepends = Annotated[
    CategoryService, Depends(get_category_service)
]
