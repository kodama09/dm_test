from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ActivatedUserDTO:
    id: UUID
    email: str
    status: str
    activated_at: datetime
