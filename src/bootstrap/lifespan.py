from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.settings import get_settings
from src.infrastructure.database.migration_runner import run_migrations
from src.infrastructure.database.postgres_pool import create_postgres_pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    postgres_pool = await create_postgres_pool(settings)
    app.state.postgres_pool = postgres_pool

    try:
        await run_migrations(postgres_pool)
        yield
    finally:
        await postgres_pool.close()
