from dataclasses import dataclass, field
from datetime import datetime, time
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from src.domain.common.models import Entity
from src.domain.supplier.models import Address


class DayOfWeek(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class TransferStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"
    CANCELLED = "cancelled"


@dataclass
class OperatingHours:
    open_time: time
    close_time: time
    days_open: List[DayOfWeek]

    @property
    def is_open_now(self) -> bool:
        from datetime import datetime as dt

        now = dt.now()
        current_time = now.time()
        current_day = DayOfWeek(now.strftime("%A").lower())

        if current_day not in self.days_open:
            return False

        return self.open_time <= current_time <= self.close_time

    @property
    def operating_hours_str(self) -> str:
        return f"{self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"


@dataclass
class StorageLocation:
    warehouse_id: str
    zone: str
    aisle: str
    shelf: str
    bin: str
    capacity_units: int
    current_units: int
    item_type: str
    location_id: Optional[str] = None
    temperature_controlled: bool = False
    hazardous: bool = False

    def __post_init__(self) -> None:
        if self.location_id is None:
            self.location_id = str(uuid4())

    @property
    def available_capacity(self) -> int:
        return self.capacity_units - self.current_units

    @property
    def utilization_percentage(self) -> float:
        if self.capacity_units == 0:
            return 0.0
        return (self.current_units / self.capacity_units) * 100

    @property
    def location_code(self) -> str:
        return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin}"

    def can accommodate(self, quantity: int) -> bool:
        return self.available_capacity >= quantity


@dataclass
class Warehouse(Entity):
    name: str
    location: Address
    capacity_sqm: float
    utilized_sqm: float
    manager_id: str
    operating_hours: OperatingHours
    warehouse_type: str = "distribution"  # distribution, fulfillment, cold_storage
    active: bool = True
    phone: Optional[str] = None
    email: Optional[str] = None
    temperature_controlled: bool = False
    security_level: str = "standard"  # standard, high, maximum

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def utilization_percentage(self) -> float:
        if self.capacity_sqm == 0:
            return 0.0
        return (self.utilized_sqm / self.capacity_sqm) * 100

    @property
    def available_capacity_sqm(self) -> float:
        return self.capacity_sqm - self.utilized_sqm

    @property
    def is_at_capacity(self) -> bool:
        return self.utilized_sqm >= self.capacity_sqm

    @property
    def is_near_capacity(self, threshold: float = 0.9) -> bool:
        return self.utilization_percentage >= (threshold * 100)


@dataclass
class TransferItem:
    item_id: str
    quantity: int
    sku: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.item_id and self.quantity > 0


@dataclass
class WarehouseTransfer(Entity):
    from_warehouse_id: str
    to_warehouse_id: str
    items: List[TransferItem]
    status: TransferStatus
    initiated_by: str
    initiated_at: datetime
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    shipment_id: Optional[str] = None
    received_by: Optional[str] = None
    received_at: Optional[datetime] = None
    notes: Optional[str] = None
    estimated_arrival: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def total_items(self) -> int:
        return len(self.items)

    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def can_be_approved(self) -> bool:
        return self.status == TransferStatus.PENDING

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [TransferStatus.PENDING, TransferStatus.APPROVED]

    @property
    def is_complete(self) -> bool:
        return self.status == TransferStatus.RECEIVED
