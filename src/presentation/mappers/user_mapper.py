from fastapi.security import HTTPBasicCredentials

from src.application.commands.activate_user_command import ActivateUserCommand
from src.application.commands.register_user_command import RegisterUserCommand
from src.application.dto.activated_user_dto import ActivatedUserDTO
from src.application.dto.registered_user_dto import RegisteredUserDTO
from src.presentation.schemas.requests.activate_user_request import ActivateUserRequest
from src.presentation.schemas.requests.register_user_request import RegisterUserRequest
from src.presentation.schemas.responses.user_response import UserResponse


def map_activate_user_request_to_command(
    request: ActivateUserRequest,
    credentials: HTTPBasicCredentials,
) -> ActivateUserCommand:
    return ActivateUserCommand(
        email=credentials.username,
        password=credentials.password,
        activation_code=request.activation_code,
    )


def map_register_user_request_to_command(
    request: RegisterUserRequest,
) -> RegisterUserCommand:
    return RegisterUserCommand(
        email=request.email,
        password=request.password,
    )


def map_registered_user_dto_to_response(dto: RegisteredUserDTO) -> UserResponse:
    return UserResponse(
        id=dto.id,
        email=dto.email,
        status=dto.status,
    )


def map_activated_user_dto_to_response(dto: ActivatedUserDTO) -> UserResponse:
    return UserResponse(
        id=dto.id,
        email=dto.email,
        status=dto.status,
    )
