from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ActivationCode:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) != 4 or not self.value.isdigit():
            raise ValueError("Activation code must contain exactly 4 digits")

    def __str__(self) -> str:
        return self.value
