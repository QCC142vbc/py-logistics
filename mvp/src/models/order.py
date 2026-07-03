from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    item_id: str
    sku: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * Decimal(self.quantity)


class Order(BaseModel):
    id: Optional[str] = None
    customer_id: str = Field(..., min_length=1)
    order_date: Optional[datetime] = None
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItem] = Field(default_factory=list)
    total_amount: Optional[Decimal] = None
    shipping_address: Optional[str] = None
    created_at: Optional[datetime] = None

    @property
    def can_be_cancelled(self) -> bool:
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    @property
    def is_complete(self) -> bool:
        return self.status == OrderStatus.DELIVERED

    def calculate_total(self) -> Decimal:
        self.total_amount = sum(item.subtotal for item in self.items)
        return self.total_amount

    class Config:
        from_attributes = True
