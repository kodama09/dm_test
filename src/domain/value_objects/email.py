from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized_value = self.value.strip().lower()

        if "@" not in normalized_value:
            raise ValueError("Email must contain an @ sign")

        local_part, domain_part = normalized_value.rsplit("@", maxsplit=1)

        if not local_part or not domain_part or "." not in domain_part:
            raise ValueError("Email must be valid")

        object.__setattr__(self, "value", normalized_value)

    def __str__(self) -> str:
        return self.value
