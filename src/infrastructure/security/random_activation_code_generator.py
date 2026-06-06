import secrets

from src.domain.value_objects.activation_code import ActivationCode


class RandomActivationCodeGenerator:
    def generate(self) -> ActivationCode:
        return ActivationCode(f"{secrets.randbelow(10_000):04d}")
