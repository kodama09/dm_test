from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from src.application.commands.activate_user_command import ActivateUserCommand
from src.application.dto.activated_user_dto import ActivatedUserDTO
from src.bootstrap.dependencies import get_activate_user_use_case

pytestmark = [pytest.mark.anyio, pytest.mark.functional]


async def test_activation_endpoint_returns_activated_user(app, http_client) -> None:
    app.dependency_overrides[get_activate_user_use_case] = (
        lambda: StubActivateUseCase()
    )

    response = await http_client.post(
        "/users/activate",
        auth=("ada@example.com", "CorrectHorse123"),
        json={"activation_code": "1234"},
    )

    assert response.status_code == 200
    body = response.json()
    assert UUID(body["id"])
    assert body["email"] == "ada@example.com"
    assert body["status"] == "activated"


class StubActivateUseCase:
    async def execute(self, command: ActivateUserCommand) -> ActivatedUserDTO:
        return ActivatedUserDTO(
            id=uuid4(),
            email=command.email,
            status="activated",
            activated_at=datetime.now(UTC),
        )
