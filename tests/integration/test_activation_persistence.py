from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.domain.entities.user import User, UserStatus
from src.domain.value_objects.email import Email
from src.infrastructure.database.postgres_user_repository import PostgresUserRepository

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_postgres_user_repository_persists_activation(postgres_pool) -> None:
    repository = PostgresUserRepository(postgres_pool)
    user = User(
        id=uuid4(),
        email=Email("ada@example.com"),
        password_hash="password-hash",
        activation_code_hash="activation-code-hash",
        activation_code_expires_at=datetime.now(UTC) + timedelta(minutes=1),
        status=UserStatus.PENDING_ACTIVATION,
        created_at=datetime.now(UTC),
    )

    await repository.save(user)
    user.activate(datetime.now(UTC))
    await repository.update(user)

    loaded_user = await repository.get_by_email(Email("ada@example.com"))

    assert loaded_user is not None
    assert loaded_user.status is UserStatus.ACTIVATED
    assert loaded_user.activated_at == user.activated_at
