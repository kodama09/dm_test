from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions.account_activation_errors import (
    AccountAlreadyActivatedError,
    ExpiredActivationCodeError,
    InvalidActivationCodeError,
    InvalidCredentialsError,
)
from src.application.exceptions.user_registration_errors import (
    EmailAlreadyRegisteredError,
)
from src.presentation.schemas.responses.error_response import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EmailAlreadyRegisteredError,
        _email_already_registered_handler,
    )
    app.add_exception_handler(
        InvalidCredentialsError,
        _invalid_credentials_handler,
    )
    app.add_exception_handler(
        InvalidActivationCodeError,
        _invalid_activation_code_handler,
    )
    app.add_exception_handler(
        ExpiredActivationCodeError,
        _expired_activation_code_handler,
    )
    app.add_exception_handler(
        AccountAlreadyActivatedError,
        _account_already_activated_handler,
    )


async def _email_already_registered_handler(
    _request: Request,
    _exc: EmailAlreadyRegisteredError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email is already registered",
    )


async def _invalid_credentials_handler(
    _request: Request,
    _exc: InvalidCredentialsError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


async def _invalid_activation_code_handler(
    _request: Request,
    _exc: InvalidActivationCodeError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid activation code",
    )


async def _expired_activation_code_handler(
    _request: Request,
    _exc: ExpiredActivationCodeError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Activation code has expired",
    )


async def _account_already_activated_handler(
    _request: Request,
    _exc: AccountAlreadyActivatedError,
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_409_CONFLICT,
        detail="Account is already activated",
    )


def _error_response(
    status_code: int,
    detail: str,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    content = ErrorResponse(detail=detail).model_dump()

    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=headers,
    )
