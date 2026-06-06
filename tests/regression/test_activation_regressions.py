import pytest

from src.application.commands.activate_user_command import ActivateUserCommand
from src.application.exceptions.account_activation_errors import (
    AccountAlreadyActivatedError,
    ExpiredActivationCodeError,
    InvalidActivationCodeError,
    InvalidCredentialsError,
)
from src.application.use_cases.activate_user import ActivateUserUseCase
from src.bootstrap.dependencies import get_activate_user_use_case
from src.domain.entities.user import User
from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email
from tests.helpers import RecordingPasswordHasher, StaticClock

pytestmark = [pytest.mark.anyio, pytest.mark.regression]


async def test_activation_checks_password_hash_even_when_user_is_missing() -> None:
    password_hasher = RecordingPasswordHasher()
    use_case = ActivateUserUseCase(
        user_repository=MissingUserRepository(),
        password_hasher=password_hasher,
        activation_code_hasher=UnusedActivationCodeHasher(),
        clock=StaticClock(),
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            ActivateUserCommand(
                email="missing@example.com",
                password="CorrectHorse123",
                activation_code="1234",
            ),
        )

    assert password_hasher.verified_hashes == ["dummy-hash"]


@pytest.mark.parametrize(
    ("exception", "expected_status", "expected_detail"),
    [
        (InvalidCredentialsError(), 401, "Invalid credentials"),
        (
            InvalidActivationCodeError(Email("ada@example.com")),
            400,
            "Invalid activation code",
        ),
        (
            ExpiredActivationCodeError(Email("ada@example.com")),
            400,
            "Activation code has expired",
        ),
        (
            AccountAlreadyActivatedError(Email("ada@example.com")),
            409,
            "Account is already activated",
        ),
    ],
)
async def test_activation_errors_return_stable_http_responses(
    app,
    http_client,
    exception,
    expected_status: int,
    expected_detail: str,
) -> None:
    app.dependency_overrides[get_activate_user_use_case] = (
        lambda: RaisingActivateUseCase(exception)
    )

    response = await http_client.post(
        "/users/activate",
        auth=("ada@example.com", "CorrectHorse123"),
        json={"activation_code": "1234"},
    )

    assert response.status_code == expected_status
    assert response.json() == {"detail": expected_detail}


class MissingUserRepository:
    async def exists_by_email(self, email: Email) -> bool:
        return False

    async def get_by_email(self, email: Email) -> User | None:
        return None

    async def save(self, user: User) -> None:
        raise AssertionError("save should not be called")

    async def update(self, user: User) -> None:
        raise AssertionError("update should not be called")


class UnusedActivationCodeHasher:
    def hash(self, activation_code: ActivationCode) -> str:
        raise AssertionError("activation code should not be hashed")

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        raise AssertionError("activation code should not be verified")


class RaisingActivateUseCase:
    def __init__(self, exception: Exception) -> None:
        self._exception = exception

    async def execute(self, command: ActivateUserCommand) -> None:
        raise self._exception
