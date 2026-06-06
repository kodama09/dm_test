from datetime import UTC, datetime

from src.domain.entities.user import User
from src.domain.value_objects.activation_code import ActivationCode
from src.domain.value_objects.email import Email


class InMemoryUserRepository:
    def __init__(
        self,
        user: User | None = None,
        existing_emails: set[str] | None = None,
    ) -> None:
        self._user = user
        self._existing_emails = existing_emails or set()
        self.saved_user: User | None = None
        self.updated_user: User | None = None

    async def exists_by_email(self, email: Email) -> bool:
        return str(email) in self._known_emails

    async def get_by_email(self, email: Email) -> User | None:
        if self._user is None or str(self._user.email) != str(email):
            return None

        return self._user

    async def save(self, user: User) -> None:
        self._user = user
        self.saved_user = user
        self._existing_emails.add(str(user.email))

    async def update(self, user: User) -> None:
        self._user = user
        self.updated_user = user

    @property
    def _known_emails(self) -> set[str]:
        emails = set(self._existing_emails)

        if self._user is not None:
            emails.add(str(self._user.email))

        return emails


class StaticPasswordHasher:
    def hash(self, plain_password: str) -> str:
        return "hashed-password"

    def verify(self, plain_password: str, password_hash: str) -> bool:
        return True

    def dummy_hash(self) -> str:
        return "dummy-hash"


class RejectingPasswordHasher:
    def hash(self, plain_password: str) -> str:
        return "hashed-password"

    def verify(self, plain_password: str, password_hash: str) -> bool:
        return False

    def dummy_hash(self) -> str:
        return "dummy-hash"


class RecordingPasswordHasher:
    def __init__(self) -> None:
        self.verified_hashes: list[str] = []

    def hash(self, plain_password: str) -> str:
        return "hashed-password"

    def verify(self, plain_password: str, password_hash: str) -> bool:
        self.verified_hashes.append(password_hash)
        return False

    def dummy_hash(self) -> str:
        return "dummy-hash"


class StaticActivationCodeGenerator:
    def generate(self) -> ActivationCode:
        return ActivationCode("1234")


class StaticActivationCodeHasher:
    def hash(self, activation_code: ActivationCode) -> str:
        return f"hashed-{activation_code}"

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return activation_code_hash == self.hash(activation_code)


class RejectingActivationCodeHasher:
    def hash(self, activation_code: ActivationCode) -> str:
        return f"hashed-{activation_code}"

    def verify(
        self,
        activation_code: ActivationCode,
        activation_code_hash: str,
    ) -> bool:
        return False


class RecordingEmailSender:
    def __init__(self) -> None:
        self.sent_codes: list[tuple[str, str]] = []

    async def send_activation_code(
        self,
        email: Email,
        activation_code: ActivationCode,
    ) -> None:
        self.sent_codes.append((str(email), str(activation_code)))


class StaticClock:
    @staticmethod
    def now() -> datetime:
        return datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
