from typing import List, Optional

from src.domain.inventory.exceptions import (
    InsufficientStockError,
    InvalidSKUError,
    ItemNotFoundError,
)
from src.domain.inventory.models import Item, StockLevel, InventoryTransaction, TransactionType
from src.domain.inventory.repository import InventoryRepository, ItemFilter
from src.domain.inventory.value_objects import SKU, Quantity


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def add_item(self, item: Item) -> Item:
        """Add a new item to inventory."""
        # Validate SKU
        try:
            SKU(item.sku)
        except ValueError as e:
            raise InvalidSKUError(str(e))

        # Check if SKU already exists
        existing = await self._repository.get_item_by_sku(item.sku)
        if existing:
            raise InvalidSKUError(f"Item with SKU {item.sku} already exists")

        await self._repository.save_item(item)
        
        # Initialize stock level
        stock_level = StockLevel(
            item_id=item.id,
            available=item.quantity,
            reserved=0,
            in_transit=0,
            on_order=0,
        )
        await self._repository.update_stock_level(
            item_id=item.id,
            available_delta=item.quantity,
        )

        return item

    async def get_item(self, item_id: str) -> Item:
        """Retrieve an item by ID."""
        item = await self._repository.get_item(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        return item

    async def get_item_by_sku(self, sku: str) -> Item:
        """Retrieve an item by SKU."""
        item = await self._repository.get_item_by_sku(sku)
        if not item:
            raise ItemNotFoundError(f"Item with SKU {sku} not found")
        return item

    async def adjust_stock(
        self,
        item_id: str,
        quantity: int,
        reason: str,
        performed_by: Optional[str] = None,
    ) -> StockLevel:
        """Adjust stock level for an item."""
        item = await self.get_item(item_id)
        
        # Validate quantity
        Quantity(quantity)

        new_stock = await self._repository.update_stock_level(
            item_id=item_id,
            available_delta=quantity,
        )

        # Record transaction
        transaction = InventoryTransaction.create(
            item_id=item_id,
            transaction_type=TransactionType.ADJUSTMENT,
            quantity=quantity,
            reference_id=f"ADJUST-{item_id}",
            notes=reason,
            performed_by=performed_by,
        )
        await self._repository.record_transaction(transaction)

        return new_stock

    async def reserve_stock(
        self,
        item_id: str,
        quantity: int,
        order_id: str,
    ) -> bool:
        """Reserve stock for an order."""
        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level:
            raise ItemNotFoundError(f"Stock level for item {item_id} not found")

        if not stock_level.can_reserve(quantity):
            raise InsufficientStockError(
                f"Cannot reserve {quantity} units. Available: {stock_level.available_for_reservation}"
            )

        await self._repository.update_stock_level(
            item_id=item_id,
            reserved_delta=quantity,
        )

        # Record transaction
        transaction = InventoryTransaction.create(
            item_id=item_id,
            transaction_type=TransactionType.SHIPMENT,
            quantity=quantity,
            reference_id=order_id,
            notes=f"Reserved for order {order_id}",
        )
        await self._repository.record_transaction(transaction)

        return True

    async def release_reservation(
        self,
        item_id: str,
        quantity: int,
        order_id: str,
    ) -> bool:
        """Release a stock reservation."""
        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level:
            raise ItemNotFoundError(f"Stock level for item {item_id} not found")

        if stock_level.reserved < quantity:
            raise InsufficientStockError(
                f"Cannot release {quantity} units. Reserved: {stock_level.reserved}"
            )

        await self._repository.update_stock_level(
            item_id=item_id,
            reserved_delta=-quantity,
        )

        # Record transaction
        transaction = InventoryTransaction.create(
            item_id=item_id,
            transaction_type=TransactionType.ADJUSTMENT,
            quantity=-quantity,
            reference_id=order_id,
            notes=f"Released reservation for order {order_id}",
        )
        await self._repository.record_transaction(transaction)

        return True

    async def check_availability(self, item_id: str, quantity: int) -> bool:
        """Check if sufficient stock is available."""
        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level:
            return False
        return stock_level.can_reserve(quantity)

    async def get_low_stock_items(self, threshold: Optional[int] = None) -> List[Item]:
        """Retrieve items that are below their reorder point or threshold."""
        return await self._repository.get_low_stock_items(threshold)

    async def transfer_stock(
        self,
        item_id: str,
        from_location: str,
        to_location: str,
        quantity: int,
        performed_by: Optional[str] = None,
    ) -> bool:
        """Transfer stock between locations."""
        item = await self.get_item(item_id)
        
        # Check if item is at source location
        if item.location != from_location:
            raise ItemNotFoundError(
                f"Item {item_id} is not at location {from_location}"
            )

        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level or stock_level.available < quantity:
            raise InsufficientStockError(
                f"Insufficient stock at {from_location}. Available: {stock_level.available if stock_level else 0}"
            )

        # Decrease stock at source
        await self._repository.update_stock_level(
            item_id=item_id,
            available_delta=-quantity,
            in_transit_delta=quantity,
        )

        # Record transfer transaction
        transaction = InventoryTransaction.create(
            item_id=item_id,
            transaction_type=TransactionType.TRANSFER,
            quantity=quantity,
            reference_id=f"TRANSFER-{item_id}",
            from_location=from_location,
            to_location=to_location,
            performed_by=performed_by,
        )
        await self._repository.record_transaction(transaction)

        return True

    async def receive_transfer(
        self,
        item_id: str,
        quantity: int,
        from_location: str,
        to_location: str,
        performed_by: Optional[str] = None,
    ) -> bool:
        """Complete a stock transfer by receiving at destination."""
        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level:
            raise ItemNotFoundError(f"Stock level for item {item_id} not found")

        if stock_level.in_transit < quantity:
            raise InsufficientStockError(
                f"Cannot receive {quantity} units in transit. In transit: {stock_level.in_transit}"
            )

        # Update item location
        item = await self.get_item(item_id)
        item.location = to_location
        await self._repository.save_item(item)

        # Decrease in-transit, increase available
        await self._repository.update_stock_level(
            item_id=item_id,
            available_delta=quantity,
            in_transit_delta=-quantity,
        )

        # Record receipt transaction
        transaction = InventoryTransaction.create(
            item_id=item_id,
            transaction_type=TransactionType.RECEIPT,
            quantity=quantity,
            reference_id=f"RECEIVE-{item_id}",
            from_location=from_location,
            to_location=to_location,
            performed_by=performed_by,
        )
        await self._repository.record_transaction(transaction)

        return True

    async def list_items(self, filter: Optional[ItemFilter] = None) -> List[Item]:
        """List items based on filter criteria."""
        if filter is None:
            filter = ItemFilter()
        return await self._repository.list_items(filter)

    async def get_stock_level(self, item_id: str) -> StockLevel:
        """Retrieve the current stock level for an item."""
        stock_level = await self._repository.get_stock_level(item_id)
        if not stock_level:
            raise ItemNotFoundError(f"Stock level for item {item_id} not found")
        return stock_level
