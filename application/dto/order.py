from dataclasses import dataclass
from typing import List


@dataclass
class OrderItemDTO:
    item_id: str
    sku: str
    quantity: int
    unit_price: str
    subtotal: str


@dataclass
class OrderDTO:
    id: str
    customer_id: str
    order_date: str
    status: str
    items: List[dict]
    total_amount: str
