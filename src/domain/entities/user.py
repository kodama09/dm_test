from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from src.domain.value_objects.email import Email


class UserStatus(StrEnum):
    PENDING_ACTIVATION = "pending_activation"
    ACTIVATED = "activated"


@dataclass(slots=True)
class User:
    id: UUID
    email: Email
    password_hash: str
    activation_code_hash: str
    activation_code_expires_at: datetime
    status: UserStatus
    created_at: datetime
    activated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.password_hash:
            raise ValueError("Password hash is required")

        if not self.activation_code_hash:
            raise ValueError("Activation code hash is required")

        if self.status is UserStatus.ACTIVATED and self.activated_at is None:
            raise ValueError("Activated users must have an activation date")

        if (
            self.status is UserStatus.PENDING_ACTIVATION
            and self.activated_at is not None
        ):
            raise ValueError("Pending users cannot have an activation date")

    def activate(self, activated_at: datetime) -> None:
        if self.status is UserStatus.ACTIVATED:
            raise ValueError("User is already activated")

        self.status = UserStatus.ACTIVATED
        self.activated_at = activated_at

    def is_activation_code_expired(self, now: datetime) -> bool:
        return _as_utc(now) >= _as_utc(self.activation_code_expires_at)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)
