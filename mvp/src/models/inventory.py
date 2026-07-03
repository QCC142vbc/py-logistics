from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class Item(BaseModel):
    id: Optional[str] = None
    sku: str = Field(..., min_length=1, pattern=r"^[A-Z0-9-]+$")
    name: str = Field(..., min_length=1)
    quantity: int = Field(default=0, ge=0)
    unit_cost: Decimal = Field(default=Decimal("0.00"), ge=0)
    location: str = Field(default="WH-DEFAULT")
    category: str = Field(default="general")
    reorder_point: int = Field(default=10, ge=0)
    created_at: Optional[datetime] = None

    @property
    def is_below_reorder_point(self) -> bool:
        return self.quantity <= self.reorder_point

    @property
    def total_value(self) -> Decimal:
        return self.unit_cost * Decimal(self.quantity)

    class Config:
        from_attributes = True
