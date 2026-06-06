from datetime import timedelta
from uuid import uuid4

from src.application.commands.register_user_command import RegisterUserCommand
from src.application.dto.registered_user_dto import RegisteredUserDTO
from src.application.exceptions.user_registration_errors import (
    EmailAlreadyRegisteredError,
)
from src.application.ports.activation_code_generator import ActivationCodeGenerator
from src.application.ports.activation_code_hasher import ActivationCodeHasher
from src.application.ports.clock import Clock
from src.application.ports.email_sender import EmailSender
from src.application.ports.password_hasher import PasswordHasher
from src.application.ports.user_repository import UserRepository
from src.domain.entities.user import User, UserStatus
from src.domain.value_objects.email import Email


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        activation_code_generator: ActivationCodeGenerator,
        activation_code_hasher: ActivationCodeHasher,
        email_sender: EmailSender,
        clock: Clock,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._activation_code_generator = activation_code_generator
        self._activation_code_hasher = activation_code_hasher
        self._email_sender = email_sender
        self._clock = clock

    async def execute(self, command: RegisterUserCommand) -> RegisteredUserDTO:
        email = Email(command.email)

        if await self._user_repository.exists_by_email(email):
            raise EmailAlreadyRegisteredError(email)

        activation_code = self._activation_code_generator.generate()
        now = self._clock.now()
        user = User(
            id=uuid4(),
            email=email,
            password_hash=self._password_hasher.hash(command.password),
            activation_code_hash=self._activation_code_hasher.hash(activation_code),
            activation_code_expires_at=now + timedelta(minutes=1),
            status=UserStatus.PENDING_ACTIVATION,
            created_at=now,
        )

        await self._user_repository.save(user)
        await self._email_sender.send_activation_code(email, activation_code)

        return RegisteredUserDTO(
            id=user.id,
            email=str(user.email),
            status=user.status.value,
        )
