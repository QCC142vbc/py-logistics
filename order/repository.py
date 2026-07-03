from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.domain.order.models import Order, OrderStatus, PurchaseOrder, PurchaseOrderStatus


@dataclass
class OrderFilter:
    customer_id: Optional[str] = None
    status: Optional[OrderStatus] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None


@dataclass
class PurchaseOrderFilter:
    supplier_id: Optional[str] = None
    status: Optional[PurchaseOrderStatus] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class OrderRepository(ABC):
    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by ID."""
        pass

    @abstractmethod
    async def save_order(self, order: Order) -> None:
        """Save or update an order."""
        pass

    @abstractmethod
    async def delete_order(self, order_id: str) -> None:
        """Delete an order by ID."""
        pass

    @abstractmethod
    async def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Retrieve all orders for a customer."""
        pass

    @abstractmethod
    async def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Retrieve all orders with a specific status."""
        pass

    @abstractmethod
    async def list_orders(self, filter: OrderFilter) -> List[Order]:
        """List orders based on filter criteria."""
        pass

    @abstractmethod
    async def get_purchase_order(self, po_id: str) -> Optional[PurchaseOrder]:
        """Retrieve a purchase order by ID."""
        pass

    @abstractmethod
    async def save_purchase_order(self, po: PurchaseOrder) -> None:
        """Save or update a purchase order."""
        pass

    @abstractmethod
    async def delete_purchase_order(self, po_id: str) -> None:
        """Delete a purchase order by ID."""
        pass

    @abstractmethod
    async def get_purchase_orders_by_supplier(
        self,
        supplier_id: str,
    ) -> List[PurchaseOrder]:
        """Retrieve all purchase orders for a supplier."""
        pass

    @abstractmethod
    async def get_purchase_orders_by_status(
        self,
        status: PurchaseOrderStatus,
    ) -> List[PurchaseOrder]:
        """Retrieve all purchase orders with a specific status."""
        pass

    @abstractmethod
    async def list_purchase_orders(
        self,
        filter: PurchaseOrderFilter,
    ) -> List[PurchaseOrder]:
        """List purchase orders based on filter criteria."""
        pass

    @abstractmethod
    async def get_pending_orders(self) -> List[Order]:
        """Retrieve all pending orders."""
        pass

    @abstractmethod
    async def get_orders_ready_for_shipment(self) -> List[Order]:
        """Retrieve orders that are ready for shipment."""
        pass

    @abstractmethod
    async def get_overdue_purchase_orders(self) -> List[PurchaseOrder]:
        """Retrieve purchase orders that are overdue."""
        pass
