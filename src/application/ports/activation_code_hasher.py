from typing import Protocol

from src.domain.value_objects.activation_code import ActivationCode


class ActivationCodeHasher(Protocol):
    def hash(self, activation_code: ActivationCode) -> str:
        pass

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        pass
