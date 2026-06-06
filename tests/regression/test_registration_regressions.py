import pytest

from src.application.commands.register_user_command import RegisterUserCommand
from src.application.exceptions.user_registration_errors import (
    EmailAlreadyRegisteredError,
)
from src.bootstrap.dependencies import get_register_user_use_case
from src.domain.value_objects.email import Email

pytestmark = [pytest.mark.anyio, pytest.mark.regression]


async def test_duplicate_registration_returns_conflict(app, http_client) -> None:
    app.dependency_overrides[get_register_user_use_case] = (
        lambda: DuplicateRegisterUseCase()
    )

    response = await http_client.post(
        "/users",
        json={
            "email": "ada@example.com",
            "password": "CorrectHorse123",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email is already registered"}


class DuplicateRegisterUseCase:
    async def execute(self, command: RegisterUserCommand) -> None:
        raise EmailAlreadyRegisteredError(Email(command.email))
