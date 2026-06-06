from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.application.commands.activate_user_command import ActivateUserCommand
from src.application.exceptions.account_activation_errors import (
    AccountAlreadyActivatedError,
    ExpiredActivationCodeError,
    InvalidActivationCodeError,
    InvalidCredentialsError,
)
from src.application.use_cases.activate_user import ActivateUserUseCase
from src.domain.entities.user import User, UserStatus
from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email

pytestmark = [pytest.mark.anyio, pytest.mark.unit]


async def test_activate_user_marks_pending_user_as_activated() -> None:
    repository = InMemoryUserRepository(user=_pending_user())
    use_case = ActivateUserUseCase(
        user_repository=repository,
        password_hasher=AcceptingPasswordHasher(),
        activation_code_hasher=StaticActivationCodeHasher(),
        clock=StaticClock(),
    )

    result = await use_case.execute(_command())

    assert result.email == "ada@example.com"
    assert result.status == "activated"
    assert result.activated_at == StaticClock.now()
    assert repository.updated_user is not None
    assert repository.updated_user.status is UserStatus.ACTIVATED


async def test_activate_user_rejects_unknown_email() -> None:
    use_case = ActivateUserUseCase(
        user_repository=InMemoryUserRepository(user=None),
        password_hasher=RejectingPasswordHasher(),
        activation_code_hasher=StaticActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(_command())


async def test_activate_user_rejects_wrong_password() -> None:
    use_case = ActivateUserUseCase(
        user_repository=InMemoryUserRepository(user=_pending_user()),
        password_hasher=RejectingPasswordHasher(),
        activation_code_hasher=StaticActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(_command())


async def test_activate_user_rejects_invalid_activation_code() -> None:
    use_case = ActivateUserUseCase(
        user_repository=InMemoryUserRepository(user=_pending_user()),
        password_hasher=AcceptingPasswordHasher(),
        activation_code_hasher=RejectingActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(InvalidActivationCodeError):
        await use_case.execute(_command())


async def test_activate_user_rejects_expired_activation_code() -> None:
    use_case = ActivateUserUseCase(
        user_repository=InMemoryUserRepository(user=_pending_user(expired=True)),
        password_hasher=AcceptingPasswordHasher(),
        activation_code_hasher=StaticActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(ExpiredActivationCodeError):
        await use_case.execute(_command())


async def test_activate_user_rejects_already_activated_account() -> None:
    use_case = ActivateUserUseCase(
        user_repository=InMemoryUserRepository(user=_activated_user()),
        password_hasher=AcceptingPasswordHasher(),
        activation_code_hasher=StaticActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(AccountAlreadyActivatedError):
        await use_case.execute(_command())


def _command() -> ActivateUserCommand:
    return ActivateUserCommand(
        email="ada@example.com",
        password="CorrectHorse123",
        activation_code="1234",
    )


def _pending_user(expired: bool = False) -> User:
    expiration_delta = timedelta(minutes=-1 if expired else 1)

    return User(
        id=uuid4(),
        email=Email("ada@example.com"),
        password_hash="hashed-password",
        activation_code_hash="hashed-1234",
        activation_code_expires_at=StaticClock.now() + expiration_delta,
        status=UserStatus.PENDING_ACTIVATION,
        created_at=StaticClock.now(),
    )


def _activated_user() -> User:
    return User(
        id=uuid4(),
        email=Email("ada@example.com"),
        password_hash="hashed-password",
        activation_code_hash="hashed-1234",
        activation_code_expires_at=StaticClock.now() + timedelta(minutes=1),
        status=UserStatus.ACTIVATED,
        created_at=StaticClock.now(),
        activated_at=StaticClock.now(),
    )


class InMemoryUserRepository:
    def __init__(self, user: User | None) -> None:
        self._user = user
        self.updated_user: User | None = None

    async def exists_by_email(self, email) -> bool:
        return self._user is not None and str(self._user.email) == str(email)

    async def get_by_email(self, email) -> User | None:
        if self._user is None or str(self._user.email) != str(email):
            return None

        return self._user

    async def save(self, user) -> None:
        self._user = user

    async def update(self, user: User) -> None:
        self.updated_user = user


class AcceptingPasswordHasher:
    def verify(self, plain_password: str, password_hash: str) -> bool:
        return True

    def dummy_hash(self) -> str:
        return "dummy-hash"


class RejectingPasswordHasher:
    def verify(self, plain_password: str, password_hash: str) -> bool:
        return False

    def dummy_hash(self) -> str:
        return "dummy-hash"


class StaticActivationCodeHasher:
    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return activation_code_hash == f"hashed-{activation_code}"


class RejectingActivationCodeHasher:
    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return False


class StaticClock:
    @staticmethod
    def now() -> datetime:
        return datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
