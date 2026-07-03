from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from src.domain.common.models import Entity, Location


class TransportMode(Enum):
    TRUCK = "truck"
    RAIL = "rail"
    AIR = "air"
    SEA = "sea"
    MULTIMODAL = "multimodal"


class ShipmentStatus(Enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


@dataclass
class CarrierService:
    service_type: str
    base_rate: Decimal
    rate_per_km: Decimal
    max_weight_kg: float
    max_volume_m3: Optional[float] = None

    @property
    def service_name(self) -> str:
        return self.service_type.replace("_", " ").title()


@dataclass
class Carrier(Entity):
    name: str
    contact_email: str
    phone: str
    services: List[CarrierService]
    rating: float
    active: bool = True
    website: Optional[str] = None
    account_number: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Validate rating
        if not 0 <= self.rating <= 5:
            raise ValueError("Rating must be between 0 and 5")

    def get_service(self, service_type: str) -> Optional[CarrierService]:
        """Get a specific service by type."""
        for service in self.services:
            if service.service_type == service_type:
                return service
        return None


@dataclass
class Route(Entity):
    origin: Location
    destination: Location
    distance_km: float
    estimated_duration_hours: float
    cost: Decimal
    transport_mode: TransportMode
    waypoints: List[Location] = field(default_factory=list)
    carrier_id: Optional[str] = None
    active: bool = True

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def total_distance(self) -> float:
        """Calculate total distance including waypoints."""
        if not self.waypoints:
            return self.distance_km
        
        total = self.distance_km
        # In a real implementation, this would calculate distances between waypoints
        return total

    @property
    def total_duration(self) -> float:
        """Calculate total duration including waypoints."""
        if not self.waypoints:
            return self.estimated_duration_hours
        
        # In a real implementation, this would calculate durations between waypoints
        return self.estimated_duration_hours


@dataclass
class ShipmentItem:
    shipment_id: str
    item_id: str
    quantity: int
    weight_kg: float
    volume_m3: Optional[float] = None

    @property
    def total_weight(self) -> float:
        return self.weight_kg * self.quantity


@dataclass
class Shipment(Entity):
    order_id: str
    route_id: str
    carrier: str
    tracking_number: str
    status: ShipmentStatus
    estimated_arrival: datetime
    items: List[ShipmentItem]
    actual_arrival: Optional[datetime] = None
    pickup_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    current_location: Optional[Location] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None
    declared_value: Optional[Decimal] = None
    insurance: bool = False

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def total_weight(self) -> float:
        return sum(item.total_weight for item in self.items)

    @property
    def total_volume(self) -> float:
        return sum(item.volume_m3 or 0 for item in self.items)

    @property
    def is_delayed(self) -> bool:
        if self.actual_arrival:
            return self.actual_arrival > self.estimated_arrival
        return False

    @property
    def days_in_transit(self) -> Optional[int]:
        if self.pickup_date:
            end_date = self.actual_arrival or datetime.utcnow()
            return (end_date - self.pickup_date).days
        return None

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [ShipmentStatus.PENDING, ShipmentStatus.PICKED_UP]
