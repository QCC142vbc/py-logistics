from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from src.domain.common.models import Entity
from src.domain.supplier.models import Address


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PurchaseOrderStatus(Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    PARTIAL_RECEIVED = "partial_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    item_id: str
    sku: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)


@dataclass
class Order(Entity):
    customer_id: str
    order_date: datetime
    status: OrderStatus
    items: List[OrderItem]
    total_amount: Decimal
    shipping_address: Address
    billing_address: Address
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    payment_method: Optional[str] = None
    payment_status: str = "pending"
    shipment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    notes: Optional[str] = None
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    @property
    def can_be_processed(self) -> bool:
        return self.status == OrderStatus.CONFIRMED

    @property
    def is_fulfilled(self) -> bool:
        return self.status == OrderStatus.DELIVERED

    def calculate_total(self) -> Decimal:
        subtotal = sum(item.subtotal for item in self.items)
        return subtotal - self.discount_amount + self.tax_amount


@dataclass
class PurchaseOrderItem:
    item_id: str
    quantity: int
    unit_price: Decimal
    expected_delivery_date: Optional[date] = None
    received_quantity: int = 0

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)

    @property
    def is_fully_received(self) -> bool:
        return self.received_quantity >= self.quantity

    @property
    def pending_quantity(self) -> int:
        return max(0, self.quantity - self.received_quantity)


@dataclass
class PurchaseOrder(Entity):
    supplier_id: str
    order_date: datetime
    status: PurchaseOrderStatus
    items: List[PurchaseOrderItem]
    total_amount: Decimal
    expected_delivery: Optional[date] = None
    actual_delivery: Optional[date] = None
    supplier_reference: Optional[str] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [PurchaseOrderStatus.DRAFT, PurchaseOrderStatus.SENT]

    @property
    def can_be_received(self) -> bool:
        return self.status in [
            PurchaseOrderStatus.ACKNOWLEDGED,
            PurchaseOrderStatus.PARTIAL_RECEIVED,
        ]

    @property
    def is_fully_received(self) -> bool:
        return all(item.is_fully_received for item in self.items)

    @property
    def total_received_quantity(self) -> int:
        return sum(item.received_quantity for item in self.items)

    @property
    def total_ordered_quantity(self) -> int:
        return sum(item.quantity for item in self.items)
