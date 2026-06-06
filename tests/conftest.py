from collections.abc import AsyncIterator

import asyncpg
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.bootstrap.app import create_app
from src.config.settings import Settings
from src.infrastructure.database.migration_runner import run_migrations

TEST_DATABASE_NAME = "user_registration_test"


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def http_client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture
async def postgres_pool() -> AsyncIterator[asyncpg.Pool]:
    await _ensure_test_database()
    settings = Settings(
        app_env="test",
        postgres_db=TEST_DATABASE_NAME,
        postgres_pool_min_size=1,
        postgres_pool_max_size=2,
    )
    pool = await asyncpg.create_pool(
        dsn=settings.postgres_dsn,
        min_size=settings.postgres_pool_min_size,
        max_size=settings.postgres_pool_max_size,
        command_timeout=settings.postgres_pool_command_timeout,
    )

    try:
        await run_migrations(pool)
        await _truncate_users(pool)
        yield pool
    finally:
        await _truncate_users(pool)
        await pool.close()


async def _ensure_test_database() -> None:
    settings = Settings()

    try:
        connection = await asyncpg.connect(dsn=settings.postgres_dsn)
        exists = await connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)",
            TEST_DATABASE_NAME,
        )

        if not exists:
            await connection.execute(f'CREATE DATABASE "{TEST_DATABASE_NAME}"')
    except OSError as exc:
        pytest.skip(f"PostgreSQL is not available for integration tests: {exc}")
    finally:
        if "connection" in locals():
            await connection.close()


async def _truncate_users(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as connection:
        await connection.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
