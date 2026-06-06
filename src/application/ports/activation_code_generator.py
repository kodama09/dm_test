from typing import Protocol

from src.domain.value_objects.activation_code import ActivationCode


class ActivationCodeGenerator(Protocol):
    def generate(self) -> ActivationCode:
        ...
