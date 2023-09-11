from typing import Annotated

from fastapi import Depends

from backend.src.repositories import UserRepository
from backend.src.services import UserService


def get_user_service():
    return UserService(UserRepository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]


