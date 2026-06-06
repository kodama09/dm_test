import base64
import hashlib
import hmac
import secrets


class PBKDF2PasswordHasher:
    _algorithm = "pbkdf2_sha256"
    _iterations = 600_000
    _salt_size = 16

    def __init__(self) -> None:
        self._dummy_hash = self.hash("dummy-password")

    def hash(self, plain_password: str) -> str:
        salt = secrets.token_bytes(self._salt_size)
        password_hash = self._hash_password(plain_password, salt, self._iterations)

        return "$".join(
            [
                self._algorithm,
                str(self._iterations),
                _encode(salt),
                _encode(password_hash),
            ],
        )

    def verify(self, plain_password: str, password_hash: str) -> bool:
        algorithm, iterations, salt, expected_hash = password_hash.split(
            "$",
            maxsplit=3,
        )

        if algorithm != self._algorithm:
            return False

        computed_hash = self._hash_password(
            plain_password,
            _decode(salt),
            int(iterations),
        )

        return hmac.compare_digest(_encode(computed_hash), expected_hash)

    def dummy_hash(self) -> str:
        return self._dummy_hash

    @staticmethod
    def _hash_password(
        plain_password: str,
        salt: bytes,
        iterations: int,
    ) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            iterations,
        )


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value.encode("ascii"))
