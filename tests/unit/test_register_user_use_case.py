from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.application.commands.register_user_command import RegisterUserCommand
from src.application.exceptions.user_registration_errors import (
    EmailAlreadyRegisteredError,
)
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.value_objects.activation_code import ActivationCode

pytestmark = [pytest.mark.anyio, pytest.mark.unit]


async def test_register_user_creates_pending_user_and_sends_code() -> None:
    repository = InMemoryUserRepository()
    email_sender = RecordingEmailSender()
    use_case = RegisterUserUseCase(
        user_repository=repository,
        password_hasher=StaticPasswordHasher(),
        activation_code_generator=StaticActivationCodeGenerator(),
        activation_code_hasher=StaticActivationCodeHasher(),
        email_sender=email_sender,
        clock=StaticClock(),
    )

    result = await use_case.execute(
        RegisterUserCommand(
            email="ada@example.com",
            password="CorrectHorse123",
        ),
    )

    assert isinstance(result.id, UUID)
    assert result.email == "ada@example.com"
    assert result.status == "pending_activation"
    assert repository.saved_user is not None
    assert repository.saved_user.password_hash == "hashed-password"
    assert repository.saved_user.activation_code_hash == "hashed-1234"
    assert email_sender.sent_codes == [("ada@example.com", "1234")]


async def test_register_user_rejects_duplicate_email() -> None:
    repository = InMemoryUserRepository(existing_emails={"ada@example.com"})
    use_case = RegisterUserUseCase(
        user_repository=repository,
        password_hasher=StaticPasswordHasher(),
        activation_code_generator=StaticActivationCodeGenerator(),
        activation_code_hasher=StaticActivationCodeHasher(),
        email_sender=RecordingEmailSender(),
        clock=StaticClock(),
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        await use_case.execute(
            RegisterUserCommand(
                email="ada@example.com",
                password="CorrectHorse123",
            ),
        )


class InMemoryUserRepository:
    def __init__(self, existing_emails: set[str] | None = None) -> None:
        self._existing_emails = existing_emails or set()
        self.saved_user = None

    async def exists_by_email(self, email) -> bool:
        return str(email) in self._existing_emails

    async def get_by_email(self, email):
        return None

    async def save(self, user) -> None:
        self.saved_user = user
        self._existing_emails.add(str(user.email))

    async def update(self, user) -> None:
        self.saved_user = user


class StaticPasswordHasher:
    def hash(self, plain_password: str) -> str:
        return "hashed-password"

    def verify(self, plain_password: str, password_hash: str) -> bool:
        return True

    def dummy_hash(self) -> str:
        return "dummy-hash"


class StaticActivationCodeGenerator:
    def generate(self) -> ActivationCode:
        return ActivationCode("1234")


class StaticActivationCodeHasher:
    def hash(self, activation_code: ActivationCode) -> str:
        return f"hashed-{activation_code}"

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return activation_code_hash == self.hash(activation_code)


class RecordingEmailSender:
    def __init__(self) -> None:
        self.sent_codes: list[tuple[str, str]] = []

    async def send_activation_code(
        self,
        email,
        activation_code: ActivationCode,
    ) -> None:
        self.sent_codes.append((str(email), str(activation_code)))


class StaticClock:
    def now(self) -> datetime:
        return datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
