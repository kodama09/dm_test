from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.settings import get_settings
from src.infrastructure.database.migration_runner import run_migrations
from src.infrastructure.database.postgres_pool import create_postgres_pool
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    postgres_pool = await create_postgres_pool(settings)
    app.state.postgres_pool = postgres_pool

    try:
        await run_migrations(postgres_pool)
        app.state.user_repository = PostgresUserRepository(postgres_pool)
        app.state.password_hasher = PBKDF2PasswordHasher()
        app.state.activation_code_generator = RandomActivationCodeGenerator(
            settings.activation_code_length,
        )
        app.state.activation_code_hasher = HMACActivationCodeHasher(
            settings.activation_code_secret,
        )
        app.state.email_sender = ConsoleEmailSender()
        app.state.clock = UTCClock()
        yield
    finally:
        await postgres_pool.close()
