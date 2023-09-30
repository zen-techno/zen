from logging import getLogger

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    ASGIApp,
    BaseHTTPMiddleware,
    Request,
    RequestResponseEndpoint,
    Response,
)

logger = getLogger("ErrorHandlingMiddleware")


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception(exc)
            return JSONResponse(
                {"detail": "Internal server error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response
