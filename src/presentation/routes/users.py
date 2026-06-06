from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.application.use_cases.activate_user import ActivateUserUseCase
from src.application.use_cases.register_user import RegisterUserUseCase
from src.bootstrap.dependencies import (
    get_activate_user_use_case,
    get_register_user_use_case,
)
from src.presentation.mappers.user_mapper import (
    map_activate_user_request_to_command,
    map_activated_user_dto_to_response,
    map_register_user_request_to_command,
    map_registered_user_dto_to_response,
)
from src.presentation.schemas.requests.activate_user_request import ActivateUserRequest
from src.presentation.schemas.requests.register_user_request import RegisterUserRequest
from src.presentation.schemas.responses.user_response import UserResponse

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBasic()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterUserRequest,
    use_case: Annotated[
        RegisterUserUseCase,
        Depends(get_register_user_use_case),
    ],
) -> UserResponse:
    command = map_register_user_request_to_command(request)
    registered_user = await use_case.execute(command)

    return map_registered_user_dto_to_response(registered_user)


@router.post("/activate", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def activate_user(
    request: ActivateUserRequest,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    use_case: Annotated[
        ActivateUserUseCase,
        Depends(get_activate_user_use_case),
    ],
) -> UserResponse:
    command = map_activate_user_request_to_command(request, credentials)
    activated_user = await use_case.execute(command)

    return map_activated_user_dto_to_response(activated_user)
