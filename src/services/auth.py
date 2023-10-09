from datetime import datetime, timedelta
from logging import getLogger
from uuid import UUID

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from redis import Redis

from src.core.unit_of_work import AbstractUnitOfWork
from src.dataclasses import User
from src.exceptions.repositories import (
    RepositoryError,
    RepositoryIntegrityError,
)
from src.exceptions.services import (
    AuthServiceBadRequest,
    AuthServiceJWTError,
    AuthServiceJWTExpiredSignature,
    ServiceBadRequestError,
    ServiceError,
    UserServiceNotFoundError,
)
from src.schemas.tokens import TokensSchema
from src.schemas.users import UserCreateSchema, UserDetailReadSchema
from src.settings import settings

pwd_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = getLogger("AuthService")


class AuthService:
    @staticmethod
    async def register_user(
        *, uow: AbstractUnitOfWork, user: UserCreateSchema
    ) -> UserDetailReadSchema:
        user_dict = user.model_dump()
        password = user_dict.pop("password")
        hashed_password = pwd_crypt_context.hash(password.get_secret_value())
        try:
            async with uow:
                created_user = await uow.users.add_one(
                    data={**user_dict, "password": hashed_password}
                )
                await uow.commit()
                return created_user.to_detail_read_schema()

        except RepositoryIntegrityError as exc:
            logger.exception(exc)
            raise ServiceBadRequestError from exc
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @classmethod
    async def authenticate_user_by_email(
        cls, *, uow: AbstractUnitOfWork, redis: Redis, email: str, password: str
    ) -> TokensSchema:
        try:
            async with uow:
                user = await uow.users.get_one(email=email)
                if user is None:
                    await uow.rollback()
                    raise AuthServiceBadRequest

            return await cls._authenticate_user(
                redis=redis, user=user, password=password
            )
        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @classmethod
    async def get_detail_user_by_id(
        cls, *, uow: AbstractUnitOfWork, user_id: UUID
    ) -> UserDetailReadSchema:
        try:
            async with uow:
                user = await uow.users.get_one(id=user_id)
                if user is None:
                    await uow.rollback()
                    raise UserServiceNotFoundError
                return user.to_detail_read_schema()

        except RepositoryError as exc:
            logger.exception(exc)
            raise ServiceError from exc

    @classmethod
    async def refresh_tokens(
        cls, *, uow: AbstractUnitOfWork, redis: Redis, tokens: TokensSchema
    ) -> TokensSchema:
        user_id = await cls.validate_refresh_token(
            uow=uow,
            redis=redis,
            token=tokens.refresh_token,
            access_token=tokens.access_token,
        )
        return await cls._create_tokens(redis=redis, user_id=user_id)

    @staticmethod
    async def logout_user(
        *,
        redis: Redis,
        user_id: UUID,
    ) -> None:
        await redis.delete(str(user_id))

    @classmethod
    async def _authenticate_user(
        cls,
        *,
        redis: Redis,
        user: User,
        password: str,
    ) -> TokensSchema:
        is_valid = pwd_crypt_context.verify(
            secret=password,
            hash=user.password,
        )
        if not is_valid:
            raise AuthServiceBadRequest
        return await cls._create_tokens(redis=redis, user_id=user.id)

    @staticmethod
    def _create_access_token(*, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.auth.access_token_expire),
        }
        return jwt.encode(
            claims=payload,
            algorithm=settings.auth.jwt_algorithm,
            key=settings.auth.jwt_secret.get_secret_value(),
        )

    @staticmethod
    def _create_refresh_token(*, access_token: str) -> str:
        payload = {
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.auth.refresh_token_expire),
        }
        return jwt.encode(
            claims=payload,
            algorithm=settings.auth.jwt_algorithm,
            key=settings.auth.jwt_secret.get_secret_value(),
            access_token=access_token,
        )

    @classmethod
    async def _create_tokens(
        cls, *, redis: Redis, user_id: UUID
    ) -> TokensSchema:
        access_token = cls._create_access_token(user_id=user_id)
        refresh_token = cls._create_refresh_token(access_token=access_token)

        await redis.set(name=str(user_id), value=refresh_token)
        return TokensSchema(
            access_token=access_token, refresh_token=refresh_token
        )

    @staticmethod
    def validate_access_token(*, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.auth.jwt_secret.get_secret_value(),
                algorithms=settings.auth.jwt_algorithm,
            )
        except ExpiredSignatureError as exc:
            raise AuthServiceJWTExpiredSignature from exc
        except JWTError as exc:
            raise AuthServiceJWTError from exc

        user_id = payload.get("sub")
        if user_id is None:
            raise AuthServiceJWTError
        return UUID(user_id)

    @classmethod
    async def validate_refresh_token(
        cls,
        *,
        uow: AbstractUnitOfWork,
        redis: Redis,
        token: str,
        access_token: str,
    ) -> UUID:
        try:
            access_payload = jwt.decode(
                token=access_token,
                key=settings.auth.jwt_secret.get_secret_value(),
                algorithms=settings.auth.jwt_algorithm,
                options={"verify_exp": False},
            )
        except JWTError as exc:
            raise AuthServiceJWTError from exc

        user_id = access_payload.get("sub")
        if user_id is None:
            raise AuthServiceJWTError

        await cls.get_detail_user_by_id(uow=uow, user_id=user_id)

        try:
            jwt.decode(
                token=token,
                key=settings.auth.jwt_secret.get_secret_value(),
                access_token=access_token,
            )
        except ExpiredSignatureError as exc:
            raise AuthServiceJWTExpiredSignature from exc
        except JWTError as exc:
            raise AuthServiceJWTError from exc

        redis_token = await redis.get(user_id)
        if redis_token != token:
            raise AuthServiceJWTError

        return UUID(user_id)
