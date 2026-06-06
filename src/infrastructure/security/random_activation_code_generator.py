import secrets

from src.domain.value_objects.activation_code import ActivationCode


class RandomActivationCodeGenerator:
    def __init__(self, code_length: int = 4) -> None:
        self._code_length = code_length

    def generate(self) -> ActivationCode:
        upper_bound = 10**self._code_length

        return ActivationCode(
            f"{secrets.randbelow(upper_bound):0{self._code_length}d}",
        )
