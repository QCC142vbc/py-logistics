from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Entity:
    """Base class for all domain entities."""
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id) if self.id else 0


@dataclass
class Money:
    """Value object representing monetary amounts."""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.currency not in ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]:
            raise ValueError(f"Unsupported currency: {self.currency}")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.amount * Decimal(multiplier), self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"

    @property
    def is_zero(self) -> bool:
        return self.amount == Decimal("0")


@dataclass
class Location:
    """Value object representing a geographic location."""
    latitude: float
    longitude: float
    address: Optional[str] = None

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    def distance_to(self, other: "Location") -> float:
        """Calculate distance to another location in kilometers using Haversine formula."""
        from math import asin, cos, radians, sin, sqrt

        R = 6371  # Earth's radius in km

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        return R * c

    def __str__(self) -> str:
        if self.address:
            return self.address
        return f"({self.latitude:.4f}, {self.longitude:.4f})"
