import hashlib
import hmac

from pydantic import SecretStr

from src.domain.value_objects.activation_code import ActivationCode


class HMACActivationCodeHasher:
    def __init__(self, secret: SecretStr) -> None:
        self._secret = secret

    def hash(self, activation_code: ActivationCode) -> str:
        return hmac.new(
            self._secret.get_secret_value().encode("utf-8"),
            str(activation_code).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return hmac.compare_digest(
            self.hash(activation_code),
            activation_code_hash,
        )
