from fastapi import Request

from src.application.use_cases.register_user import RegisterUserUseCase


def get_register_user_use_case(request: Request) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        user_repository=request.app.state.user_repository,
        password_hasher=request.app.state.password_hasher,
        activation_code_generator=request.app.state.activation_code_generator,
        activation_code_hasher=request.app.state.activation_code_hasher,
        email_sender=request.app.state.email_sender,
        clock=request.app.state.clock,
    )
