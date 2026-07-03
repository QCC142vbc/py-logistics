import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SKU:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("SKU cannot be empty")
        if len(self.value) > 50:
            raise ValueError("SKU cannot exceed 50 characters")
        if not re.match(r"^[A-Z0-9-_]+$", self.value):
            raise ValueError(
                "SKU must contain only uppercase letters, numbers, hyphens, and underscores"
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Quantity cannot be negative")

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Location:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Location cannot be empty")
        if len(self.value) > 100:
            raise ValueError("Location cannot exceed 100 characters")

    def __str__(self) -> str:
        return self.value
