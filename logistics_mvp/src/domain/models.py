from dataclasses import dataclass
from typing import Optional


@dataclass
class Supplier:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""


@dataclass
class Product:
    id: Optional[int] = None
    sku: str = ""
    name: str = ""
    quantity: int = 0
    price: float = 0.0


@dataclass
class OrderItem:
    product_id: int
    sku: str
    quantity: int
    price: float


@dataclass
class Order:
    id: Optional[int] = None
    customer_id: str = ""
    items: list[OrderItem] = None
    status: str = "pending"
    total: float = 0.0

    def __post_init__(self):
        if self.items is None:
            self.items = []
