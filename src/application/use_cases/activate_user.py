from src.application.commands.activate_user_command import ActivateUserCommand
from src.application.dto.activated_user_dto import ActivatedUserDTO
from src.application.exceptions.account_activation_errors import (
    AccountAlreadyActivatedError,
    ExpiredActivationCodeError,
    InvalidActivationCodeError,
    InvalidCredentialsError,
)
from src.application.ports.activation_code_hasher import ActivationCodeHasher
from src.application.ports.clock import Clock
from src.application.ports.password_hasher import PasswordHasher
from src.application.ports.user_repository import UserRepository
from src.domain.entities.user import User, UserStatus
from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email


class ActivateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        activation_code_hasher: ActivationCodeHasher,
        clock: Clock,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._activation_code_hasher = activation_code_hasher
        self._clock = clock

    async def execute(self, command: ActivateUserCommand) -> ActivatedUserDTO:
        email = Email(command.email)
        user: User | None = await self._user_repository.get_by_email(email)
        password_hash = (
            user.password_hash if user else self._password_hasher.dummy_hash()
        )

        if not self._password_hasher.verify(command.password, password_hash):
            raise InvalidCredentialsError()

        if user is None:
            raise InvalidCredentialsError()

        if user.status is UserStatus.ACTIVATED:
            raise AccountAlreadyActivatedError(email)

        try:
            activation_code = ActivationCode(command.activation_code)
        except ValueError as exc:
            raise InvalidActivationCodeError(email) from exc
        if not self._activation_code_hasher.verify(
            activation_code,
            user.activation_code_hash,
        ):
            raise InvalidActivationCodeError(email)

        now = self._clock.now()
        if user.is_activation_code_expired(now):
            raise ExpiredActivationCodeError(email)

        user.activate(now)
        await self._user_repository.update(user)

        if user.activated_at is None:
            raise RuntimeError("Activated user must have an activation date")

        return ActivatedUserDTO(
            id=user.id,
            email=str(user.email),
            status=user.status.value,
            activated_at=user.activated_at,
        )
