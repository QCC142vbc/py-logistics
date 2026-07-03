from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import uuid4

from src.domain.common.models import Entity


@dataclass
class Address:
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    address_line2: Optional[str] = None

    def __str__(self) -> str:
        lines = [self.street]
        if self.address_line2:
            lines.append(self.address_line2)
        lines.append(f"{self.city}, {self.state} {self.postal_code}")
        lines.append(self.country)
        return "\n".join(lines)


@dataclass
class Supplier(Entity):
    name: str
    contact_email: str
    phone: str
    address: Address
    rating: float
    active: bool
    payment_terms: str
    lead_time_days: int
    contact_person: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None
    notes: Optional[str] = None
    categories: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Validate rating
        if not 0 <= self.rating <= 5:
            raise ValueError("Rating must be between 0 and 5")

    @property
    def is_preferred(self) -> bool:
        return self.rating >= 4.0


@dataclass
class SupplierScore:
    supplier_id: str
    reliability_score: float
    quality_score: float
    cost_score: float
    delivery_score: float
    overall_score: float
    last_calculated: datetime
    factors: Optional[dict] = None

    def __post_init__(self) -> None:
        if self.factors is None:
            self.factors = {}
        
        # Validate scores
        for score_name, score_value in [
            ("reliability", self.reliability_score),
            ("quality", self.quality_score),
            ("cost", self.cost_score),
            ("delivery", self.delivery_score),
            ("overall", self.overall_score),
        ]:
            if not 0 <= score_value <= 100:
                raise ValueError(f"{score_name}_score must be between 0 and 100")

    @property
    def risk_level(self) -> str:
        if self.overall_score >= 80:
            return "LOW"
        elif self.overall_score >= 60:
            return "MEDIUM"
        elif self.overall_score >= 40:
            return "HIGH"
        else:
            return "CRITICAL"


@dataclass
class SupplierContract(Entity):
    id: str
    supplier_id: str
    start_date: date
    end_date: date
    min_order_quantity: int
    unit_price: Decimal
    terms: str
    item_category: Optional[str] = None
    item_id: Optional[str] = None
    auto_renew: bool = False
    active: bool = True

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def is_expired(self) -> bool:
        return date.today() > self.end_date

    @property
    def days_until_expiry(self) -> int:
        return (self.end_date - date.today()).days

    @property
    def is_expiring_soon(self, days_threshold: int = 30) -> bool:
        return 0 <= self.days_until_expiry <= days_threshold
