from typing import List, Optional

from src.domain.inventory.exceptions import InsufficientStockError
from src.domain.inventory.services import InventoryService
from src.domain.order.exceptions import (
    InvalidOrderStatusError,
    OrderNotFoundError,
    OrderProcessingError,
)
from src.domain.order.models import (
    Order,
    OrderItem,
    OrderStatus,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseOrderStatus,
)
from src.domain.order.repository import OrderRepository, OrderFilter, PurchaseOrderFilter
from src.domain.order.validation import OrderValidator


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        inventory_service: InventoryService,
        validator: OrderValidator,
    ) -> None:
        self._order_repo = order_repo
        self._inventory_service = inventory_service
        self._validator = validator

    async def create_order(self, order: Order) -> Order:
        """Create a new order."""
        # Validate order
        validation_result = self._validator.validate_order(order)
        if not validation_result.is_valid:
            raise OrderProcessingError(f"Order validation failed: {validation_result.errors}")

        # Check item availability
        for item in order.items:
            available = await self._inventory_service.check_availability(
                item.item_id,
                item.quantity,
            )
            if not available:
                raise InsufficientStockError(
                    f"Insufficient stock for item {item.sku}"
                )

        # Set initial status
        order.status = OrderStatus.PENDING

        await self._order_repo.save_order(order)
        return order

    async def get_order(self, order_id: str) -> Order:
        """Retrieve an order by ID."""
        order = await self._order_repo.get_order(order_id)
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        return order

    async def confirm_order(self, order_id: str) -> Order:
        """Confirm an order."""
        order = await self.get_order(order_id)

        if order.status != OrderStatus.PENDING:
            raise InvalidOrderStatusError(
                f"Cannot confirm order with status {order.status}"
            )

        order.status = OrderStatus.CONFIRMED
        await self._order_repo.save_order(order)
        return order

    async def process_order(self, order_id: str) -> bool:
        """Process an order by reserving stock."""
        order = await self.get_order(order_id)

        if not order.can_be_processed:
            raise InvalidOrderStatusError(
                f"Cannot process order with status {order.status}"
            )

        # Reserve stock for all items
        for item in order.items:
            try:
                await self._inventory_service.reserve_stock(
                    item.item_id,
                    item.quantity,
                    order_id,
                )
            except InsufficientStockError as e:
                # Rollback any reservations made so far
                await self._rollback_reservations(order)
                raise OrderProcessingError(f"Failed to reserve stock: {e}")

        order.status = OrderStatus.PROCESSING
        await self._order_repo.save_order(order)
        return True

    async def cancel_order(self, order_id: str, reason: str) -> bool:
        """Cancel an order."""
        order = await self.get_order(order_id)

        if not order.can_be_cancelled:
            raise InvalidOrderStatusError(
                f"Cannot cancel order with status {order.status}"
            )

        # Release any stock reservations
        await self._rollback_reservations(order)

        order.status = OrderStatus.CANCELLED
        order.notes = f"{order.notes or if order.notes else ''}\nCancelled: {reason}"
        await self._order_repo.save_order(order)
        return True

    async def update_order_status(
        self,
        order_id: str,
        status: OrderStatus,
    ) -> Order:
        """Update the status of an order."""
        order = await self.get_order(order_id)
        order.status = status
        await self._order_repo.save_order(order)
        return order

    async def create_purchase_order(self, po: PurchaseOrder) -> PurchaseOrder:
        """Create a new purchase order."""
        po.status = PurchaseOrderStatus.DRAFT
        await self._order_repo.save_purchase_order(po)
        return po

    async def get_purchase_order(self, po_id: str) -> PurchaseOrder:
        """Retrieve a purchase order by ID."""
        po = await self._order_repo.get_purchase_order(po_id)
        if not po:
            raise OrderNotFoundError(f"Purchase order with ID {po_id} not found")
        return po

    async def send_purchase_order(self, po_id: str) -> PurchaseOrder:
        """Send a purchase order to the supplier."""
        po = await self.get_purchase_order(po_id)

        if po.status != PurchaseOrderStatus.DRAFT:
            raise InvalidOrderStatusError(
                f"Cannot send purchase order with status {po.status}"
            )

        po.status = PurchaseOrderStatus.SENT
        await self._order_repo.save_purchase_order(po)
        return po

    async def acknowledge_purchase_order(self, po_id: str) -> PurchaseOrder:
        """Acknowledge a purchase order (received from supplier)."""
        po = await self.get_purchase_order(po_id)

        if po.status != PurchaseOrderStatus.SENT:
            raise InvalidOrderStatusError(
                f"Cannot acknowledge purchase order with status {po.status}"
            )

        po.status = PurchaseOrderStatus.ACKNOWLEDGED
        await self._order_repo.save_purchase_order(po)
        return po

    async def receive_purchase_order(
        self,
        po_id: str,
        received_items: dict[str, int],
    ) -> PurchaseOrder:
        """Receive items against a purchase order."""
        po = await self.get_purchase_order(po_id)

        if not po.can_be_received:
            raise InvalidOrderStatusError(
                f"Cannot receive purchase order with status {po.status}"
            )

        # Update received quantities
        for item in po.items:
            if item.item_id in received_items:
                item.received_quantity += received_items[item.item_id]

        # Update status based on receipt
        if po.is_fully_received:
            po.status = PurchaseOrderStatus.RECEIVED
        else:
            po.status = PurchaseOrderStatus.PARTIAL_RECEIVED

        await self._order_repo.save_purchase_order(po)
        return po

    async def list_orders(
        self,
        filter: Optional[OrderFilter] = None,
    ) -> List[Order]:
        """List orders based on filter criteria."""
        if filter is None:
            filter = OrderFilter()
        return await self._order_repo.list_orders(filter)

    async def list_purchase_orders(
        self,
        filter: Optional[PurchaseOrderFilter] = None,
    ) -> List[PurchaseOrder]:
        """List purchase orders based on filter criteria."""
        if filter is None:
            filter = PurchaseOrderFilter()
        return await self._order_repo.list_purchase_orders(filter)

    async def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Retrieve all orders for a customer."""
        return await self._order_repo.get_orders_by_customer(customer_id)

    async def get_purchase_orders_by_supplier(
        self,
        supplier_id: str,
    ) -> List[PurchaseOrder]:
        """Retrieve all purchase orders for a supplier."""
        return await self._order_repo.get_purchase_orders_by_supplier(supplier_id)

    async def _rollback_reservations(self, order: Order) -> None:
        """Rollback stock reservations for an order."""
        for item in order.items:
            try:
                await self._inventory_service.release_reservation(
                    item.item_id,
                    item.quantity,
                    order.id,
                )
            except Exception:
                # Log error but continue with rollback
                pass
