from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from src.domain.inventory.models import Item, StockLevel, InventoryTransaction, TransactionType


@dataclass
class ItemFilter:
    sku: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    active_only: bool = True
    low_stock_only: bool = False
    supplier_id: Optional[str] = None


class InventoryRepository(ABC):
    @abstractmethod
    async def get_item(self, item_id: str) -> Optional[Item]:
        """Retrieve an item by its ID."""
        pass

    @abstractmethod
    async def get_item_by_sku(self, sku: str) -> Optional[Item]:
        """Retrieve an item by its SKU."""
        pass

    @abstractmethod
    async def save_item(self, item: Item) -> None:
        """Save or update an item."""
        pass

    @abstractmethod
    async def delete_item(self, item_id: str) -> None:
        """Delete an item by its ID."""
        pass

    @abstractmethod
    async def get_stock_level(self, item_id: str) -> Optional[StockLevel]:
        """Retrieve the current stock level for an item."""
        pass

    @abstractmethod
    async def update_stock_level(
        self,
        item_id: str,
        available_delta: int = 0,
        reserved_delta: int = 0,
        in_transit_delta: int = 0,
        on_order_delta: int = 0,
    ) -> StockLevel:
        """Update stock level with deltas for each component."""
        pass

    @abstractmethod
    async def list_items(self, filter: ItemFilter) -> List[Item]:
        """List items based on filter criteria."""
        pass

    @abstractmethod
    async def record_transaction(self, transaction: InventoryTransaction) -> None:
        """Record an inventory transaction."""
        pass

    @abstractmethod
    async def get_transactions(
        self,
        item_id: Optional[str] = None,
        transaction_type: Optional[TransactionType] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[InventoryTransaction]:
        """Retrieve inventory transactions with optional filters."""
        pass

    @abstractmethod
    async def get_low_stock_items(self, threshold: Optional[int] = None) -> List[Item]:
        """Retrieve items that are below their reorder point or threshold."""
        pass

    @abstractmethod
    async def get_items_by_category(self, category: str) -> List[Item]:
        """Retrieve all items in a specific category."""
        pass

    @abstractmethod
    async def get_items_by_location(self, location: str) -> List[Item]:
        """Retrieve all items at a specific location."""
        pass

    @abstractmethod
    async def get_items_by_supplier(self, supplier_id: str) -> List[Item]:
        """Retrieve all items from a specific supplier."""
        pass
