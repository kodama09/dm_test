from src.domain.value_objects.email import Email


class AccountActivationError(Exception):
    pass


class InvalidCredentialsError(AccountActivationError):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class InvalidActivationCodeError(AccountActivationError):
    def __init__(self, email: Email) -> None:
        super().__init__(f"Invalid activation code for email: {email}")
        self.email = email


class ExpiredActivationCodeError(AccountActivationError):
    def __init__(self, email: Email) -> None:
        super().__init__(f"Activation code has expired for email: {email}")
        self.email = email


class AccountAlreadyActivatedError(AccountActivationError):
    def __init__(self, email: Email) -> None:
        super().__init__(f"Account is already activated for email: {email}")
        self.email = email
