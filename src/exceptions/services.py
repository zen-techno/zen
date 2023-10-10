from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException


class BaseError(HTTPException):
    detail = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: Optional[dict[str, str]] = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class ServiceError(BaseError):
    detail = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: Optional[dict[str, str]] = None


class ServiceNotFoundError(ServiceError):
    detail = "Entity is not found"
    status_code = status.HTTP_404_NOT_FOUND


class UserServiceNotFoundError(ServiceNotFoundError):
    detail = "User is not found"


class CategoryServiceNotFoundError(ServiceNotFoundError):
    detail = "Category is not found"


class ExpenseServiceNotFoundError(ServiceNotFoundError):
    detail = "Expense is not found"


class ServiceBadRequestError(ServiceError):
    detail = "Bad request"
    status_code = status.HTTP_400_BAD_REQUEST


class AuthServiceBadRequest(ServiceBadRequestError):
    detail = "Wrong login or password"


class AuthServiceJWTError(BaseError):
    detail = "Invalid token"
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}


class AuthInvalidAccessToken(AuthServiceJWTError):
    detail = "Invalid access token"


class AuthInvalidRefreshToken(AuthServiceJWTError):
    detail = "Invalid refresh token"


class AuthExpiredAccessToken(AuthServiceJWTError):
    detail = "Expired access token signature"


class AuthExpireRefreshToken(AuthServiceJWTError):
    detail = "Expired refresh token signature"


class AuthPermissionDenied(BaseError):
    detail = "Permission denied"
    status_code = status.HTTP_403_FORBIDDEN


class AuthUserNotActive(AuthPermissionDenied):
    detail = "User not active"
