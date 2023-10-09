from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies import (
    RedisDepends,
    UnitOfWorkDepends,
    get_current_user,
)
from src.schemas.tokens import TokensSchema
from src.schemas.users import (
    UserCreateSchema,
    UserDetailReadSchema,
    UserReadSchema,
)
from src.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
async def register_user(
    uow: UnitOfWorkDepends, user: UserCreateSchema
) -> UserDetailReadSchema:
    return await AuthService.register_user(uow=uow, user=user)


@router.post(
    "/login",
    response_model=TokensSchema,
    status_code=status.HTTP_200_OK,
    summary="Email user login",
)
async def email_login_user(
    uow: UnitOfWorkDepends,
    redis: RedisDepends,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokensSchema:
    return await AuthService.authenticate_user_by_email(
        uow=uow,
        redis=redis,
        email=form_data.username,
        password=form_data.password,
    )


@router.post(
    "/logout",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="User logout",
)
async def logout_user(
    redis: RedisDepends, user: UserDetailReadSchema = Depends(get_current_user)
) -> None:
    await AuthService.logout_user(redis=redis, user_id=user.id)


@router.post(
    "/refresh-tokens",
    response_model=TokensSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
async def refresh_user_tokens(
    uow: UnitOfWorkDepends, redis: RedisDepends, tokens: TokensSchema
) -> TokensSchema:
    return await AuthService.refresh_tokens(uow=uow, redis=redis, tokens=tokens)


@router.get(
    "/me",
    response_model=UserDetailReadSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_current_user(
    user: UserDetailReadSchema = Depends(get_current_user),
) -> UserDetailReadSchema:
    return user
