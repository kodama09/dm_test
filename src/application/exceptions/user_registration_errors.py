from src.domain.value_objects.email import Email


class EmailAlreadyRegisteredError(Exception):
    def __init__(self, email: Email) -> None:
        super().__init__(f"Email is already registered: {email}")
        self.email = email
