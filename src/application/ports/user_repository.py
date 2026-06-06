from typing import Protocol

from src.domain.entities.user import User
from src.domain.value_objects.email import Email


class UserRepository(Protocol):
    async def exists_by_email(self, email: Email) -> bool:
        pass

    async def get_by_email(self, email: Email) -> User | None:
        pass

    async def save(self, user: User) -> None:
        pass
