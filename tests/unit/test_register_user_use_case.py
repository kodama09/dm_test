from uuid import UUID

import pytest

from src.application.commands.register_user_command import RegisterUserCommand
from src.application.exceptions.user_registration_errors import (
    EmailAlreadyRegisteredError,
)
from src.application.use_cases.register_user import RegisterUserUseCase
from tests.helpers import (
    InMemoryUserRepository,
    RecordingEmailSender,
    StaticActivationCodeGenerator,
    StaticActivationCodeHasher,
    StaticClock,
    StaticPasswordHasher,
)

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
