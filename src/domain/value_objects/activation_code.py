from dataclasses import dataclass

MIN_ACTIVATION_CODE_LENGTH = 4
MAX_ACTIVATION_CODE_LENGTH = 12


@dataclass(frozen=True, slots=True)
class ActivationCode:
    value: str

    def __post_init__(self) -> None:
        if not self.value.isdigit():
            raise ValueError("Activation code must contain only digits")

        if not (
            MIN_ACTIVATION_CODE_LENGTH
            <= len(self.value)
            <= MAX_ACTIVATION_CODE_LENGTH
        ):
            raise ValueError(
                "Activation code length must be between "
                f"{MIN_ACTIVATION_CODE_LENGTH} and {MAX_ACTIVATION_CODE_LENGTH} digits",
            )

    def __str__(self) -> str:
        return self.value
