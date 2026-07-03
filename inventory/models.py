from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import uuid4

from src.domain.common.models import Entity


class TransactionType(Enum):
    RECEIPT = "receipt"
    SHIPMENT = "shipment"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


@dataclass
class Item(Entity):
    sku: str
    name: str
    quantity: int
    unit_cost: Decimal
    location: str
    category: str
    reorder_point: int
    lead_time_days: int
    description: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_m3: Optional[float] = None
    supplier_id: Optional[str] = None
    active: bool = True

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def total_value(self) -> Decimal:
        return self.unit_cost * Decimal(self.quantity)

    def is_below_reorder_point(self) -> bool:
        return self.quantity <= self.reorder_point


@dataclass
class StockLevel:
    item_id: str
    available: int
    reserved: int
    in_transit: int
    on_order: int
    last_updated: datetime = field(default_factory=datetime.utcnow)

    @property
    def total_quantity(self) -> int:
        return self.available + self.reserved + self.in_transit + self.on_order

    @property
    def available_for_reservation(self) -> int:
        return self.available - self.reserved

    def can_reserve(self, quantity: int) -> bool:
        return self.available_for_reservation >= quantity


@dataclass
class InventoryTransaction:
    id: str
    item_id: str
    transaction_type: TransactionType
    quantity: int
    reference_id: str
    timestamp: datetime
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    notes: Optional[str] = None
    performed_by: Optional[str] = None

    @classmethod
    def create(
        cls,
        item_id: str,
        transaction_type: TransactionType,
        quantity: int,
        reference_id: str,
        from_location: Optional[str] = None,
        to_location: Optional[str] = None,
        notes: Optional[str] = None,
        performed_by: Optional[str] = None,
    ) -> "InventoryTransaction":
        return cls(
            id=str(uuid4()),
            item_id=item_id,
            transaction_type=transaction_type,
            quantity=quantity,
            reference_id=reference_id,
            timestamp=datetime.utcnow(),
            from_location=from_location,
            to_location=to_location,
            notes=notes,
            performed_by=performed_by,
        )
