from uuid import UUID, uuid4

import pytest

from src.application.commands.register_user_command import RegisterUserCommand
from src.application.dto.registered_user_dto import RegisteredUserDTO
from src.bootstrap.dependencies import get_register_user_use_case

pytestmark = [pytest.mark.anyio, pytest.mark.functional]


async def test_registration_endpoint_returns_created_user(app, http_client) -> None:
    app.dependency_overrides[get_register_user_use_case] = (
        lambda: StubRegisterUseCase()
    )

    response = await http_client.post(
        "/users",
        json={
            "email": "ada@example.com",
            "password": "CorrectHorse123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert UUID(body["id"])
    assert body["email"] == "ada@example.com"
    assert body["status"] == "pending_activation"


class StubRegisterUseCase:
    async def execute(self, command: RegisterUserCommand) -> RegisteredUserDTO:
        return RegisteredUserDTO(
            id=uuid4(),
            email=command.email,
            status="pending_activation",
        )
