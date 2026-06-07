from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ActivateUserCommand:
    email: str
    password: str
    activation_code: str
