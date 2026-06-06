from typing import Protocol

from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email


class EmailSender(Protocol):
    async def send_activation_code(
        self,
        email: Email,
        activation_code: ActivationCode,
    ) -> None:
        pass
