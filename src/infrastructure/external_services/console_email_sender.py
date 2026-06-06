from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email


class ConsoleEmailSender:
    async def send_activation_code(
        self,
        email: Email,
        activation_code: ActivationCode,
    ) -> None:
        print(f"Activation code for {email}: {activation_code}")
