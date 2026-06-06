import asyncpg

from src.domain.entities.user import User, UserStatus
from src.domain.value_objects.email import Email


class PostgresUserRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def exists_by_email(self, email: Email) -> bool:
        async with self._pool.acquire() as connection:
            return await connection.fetchval(
                "SELECT EXISTS(SELECT 1 FROM users WHERE email = $1)",
                str(email),
            )

    async def get_by_email(self, email: Email) -> User | None:
        async with self._pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT
                    id,
                    email,
                    password_hash,
                    activation_code_hash,
                    activation_code_expires_at,
                    status,
                    created_at,
                    activated_at
                FROM users
                WHERE email = $1
                """,
                str(email),
            )

        if row is None:
            return None

        return User(
            id=row["id"],
            email=Email(row["email"]),
            password_hash=row["password_hash"],
            activation_code_hash=row["activation_code_hash"],
            activation_code_expires_at=row["activation_code_expires_at"],
            status=UserStatus(row["status"]),
            created_at=row["created_at"],
            activated_at=row["activated_at"],
        )

    async def save(self, user: User) -> None:
        async with self._pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO users (
                    id,
                    email,
                    password_hash,
                    activation_code_hash,
                    activation_code_expires_at,
                    status,
                    created_at,
                    activated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                user.id,
                str(user.email),
                user.password_hash,
                user.activation_code_hash,
                user.activation_code_expires_at,
                user.status.value,
                user.created_at,
                user.activated_at,
            )
