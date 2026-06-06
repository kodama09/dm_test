from fastapi import Request

from src.application.use_cases.register_user import RegisterUserUseCase
from src.config.settings import get_settings
from src.infrastructure.database.postgres_user_repository import PostgresUserRepository
from src.infrastructure.external_services.console_email_sender import ConsoleEmailSender
from src.infrastructure.external_services.utc_clock import UTCClock
from src.infrastructure.security.hmac_activation_code_hasher import (
    HMACActivationCodeHasher,
)
from src.infrastructure.security.pbkdf2_password_hasher import PBKDF2PasswordHasher
from src.infrastructure.security.random_activation_code_generator import (
    RandomActivationCodeGenerator,
)


def get_register_user_use_case(request: Request) -> RegisterUserUseCase:
    settings = get_settings()

    return RegisterUserUseCase(
        user_repository=PostgresUserRepository(request.app.state.postgres_pool),
        password_hasher=PBKDF2PasswordHasher(),
        activation_code_generator=RandomActivationCodeGenerator(
            settings.activation_code_length,
        ),
        activation_code_hasher=HMACActivationCodeHasher(
            settings.activation_code_secret,
        ),
        email_sender=ConsoleEmailSender(),
        clock=UTCClock(),
    )
