from pathlib import Path

import asyncpg

MIGRATIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

MIGRATIONS_DIRECTORY = Path(__file__).parent / "migrations"


async def run_migrations(pool: asyncpg.Pool) -> None:
    migration_files = sorted(MIGRATIONS_DIRECTORY.glob("*.sql"))

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(MIGRATIONS_TABLE_SQL)

            executed_versions = await _get_executed_versions(connection)

            for migration_file in migration_files:
                version = migration_file.name

                if version in executed_versions:
                    continue

                await connection.execute(migration_file.read_text(encoding="utf-8"))
                await connection.execute(
                    "INSERT INTO schema_migrations (version) VALUES ($1)",
                    version,
                )


async def _get_executed_versions(connection: asyncpg.Connection) -> set[str]:
    rows = await connection.fetch("SELECT version FROM schema_migrations")
    return {row["version"] for row in rows}
