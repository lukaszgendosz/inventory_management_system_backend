from datetime import datetime

from fastapi import status, Request, FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import PlainTextResponse
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from jwt import PyJWTError

from app.configs.exception.error_message import ErrorMessage
from app.schemes.error import ApiErrorSchema
from app.configs.exception.exception import (
    AccessDeniedError,
    BadRequestError,
    NotFoundError,
    AuthenticationError,
    AlreadyExistsError,
)


def init_error_handler(app: FastAPI):
    @app.exception_handler(Exception)
    async def internal_server_error_handle(req: Request, exc: Exception):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000),
                date=now.isoformat(),
                msg=ErrorMessage.SOMETHING_WENT_WRONG.description,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def request_exception_handle(req: Request, exc: RequestValidationError):
        now = datetime.now()
        if exc.errors():
            msg = exc.errors()[0]["msg"]
        else:
            msg = ErrorMessage.VALIDATION_FAILED.description

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000),
                date=now.isoformat(),
                msg=msg,
            ).model_dump(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(req: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return await internal_server_error_handle(req, exc)

        return PlainTextResponse(status_code=exc.status_code)

    @app.exception_handler(NotFoundError)
    async def not_found_error_handle(req: Request, exc: NotFoundError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000), date=now.isoformat(), msg=exc.msg
            ).model_dump(),
        )

    @app.exception_handler(AlreadyExistsError)
    async def not_found_error_handle(req: Request, exc: AlreadyExistsError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000), date=now.isoformat(), msg=exc.msg
            ).model_dump(),
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_error_handle(req: Request, exc: BadRequestError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000), date=now.isoformat(), msg=exc.msg
            ).model_dump(),
        )

    @app.exception_handler(AuthenticationError)
    async def auth_error_handle(req: Request, exc: AuthenticationError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000), date=now.isoformat(), msg=exc.msg
            ).model_dump(),
        )

    @app.exception_handler(AccessDeniedError)
    async def access_denied_error_handle(req: Request, exc: AccessDeniedError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000), date=now.isoformat(), msg=exc.msg
            ).model_dump(),
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handle(req: Request, exc: IntegrityError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000),
                date=now.isoformat(),
                msg=repr(exc.args[0]),
            ).model_dump(),
        )

    @app.exception_handler(PyJWTError)
    async def jwt_token_expire_error_handle(req: Request, exc: PyJWTError):
        now = datetime.now()

        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ApiErrorSchema(
                timestamp=int(now.timestamp() * 1000),
                date=now.isoformat(),
                msg=repr(exc.args[0]),
            ).model_dump(),
        )
