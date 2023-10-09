from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.unit_of_work import UnitOfWorkDepends
from src.exceptions.services import AuthServiceJWTError
from src.schemas.users import UserDetailReadSchema
from src.services import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    uow: UnitOfWorkDepends, token: str = Depends(oauth2_scheme)
) -> UserDetailReadSchema:
    user_id = AuthService.validate_access_token(token=token)
    user = await AuthService.get_detail_user_by_id(uow=uow, user_id=user_id)
    if user is None:
        raise AuthServiceJWTError
    return user
