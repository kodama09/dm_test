import asyncpg

from src.config.settings import Settings


async def create_postgres_pool(settings: Settings) -> asyncpg.Pool:
    return await asyncpg.create_pool(dsn=settings.postgres_dsn)
