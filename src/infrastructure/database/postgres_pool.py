import asyncpg

from src.config.settings import Settings


async def create_postgres_pool(settings: Settings) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=settings.postgres_dsn,
        command_timeout=settings.postgres_pool_command_timeout,
        max_size=settings.postgres_pool_max_size,
        min_size=settings.postgres_pool_min_size,
    )
