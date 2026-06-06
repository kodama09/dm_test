from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.use_cases.register_user import RegisterUserUseCase
from src.bootstrap.dependencies import get_register_user_use_case
from src.presentation.mappers.user_mapper import (
    map_register_user_request_to_command,
    map_registered_user_dto_to_response,
)
from src.presentation.schemas.requests.register_user_request import RegisterUserRequest
from src.presentation.schemas.responses.user_response import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


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
