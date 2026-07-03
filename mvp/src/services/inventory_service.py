from typing import Optional
from src.models.inventory import Item
from src.repositories.repository import Repository


class InventoryService:
    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_item(self, item: Item) -> Item:
        # Check if SKU already exists
        existing = await self.repo.get_item_by_sku(item.sku)
        if existing:
            raise ValueError(f"Item with SKU {item.sku} already exists")
        
        item_id = await self.repo.create_item(item)
        item.id = item_id
        return item

    async def get_item(self, item_id: str) -> Optional[Item]:
        return await self.repo.get_item(item_id)

    async def get_item_by_sku(self, sku: str) -> Optional[Item]:
        return await self.repo.get_item_by_sku(sku)

    async def list_items(self) -> list[Item]:
        return await self.repo.list_items()

    async def adjust_stock(self, item_id: str, quantity_change: int) -> Optional[Item]:
        item = await self.repo.get_item(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        new_quantity = item.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Cannot have negative quantity")
        
        return await self.repo.update_item_quantity(item_id, new_quantity)

    async def get_low_stock_items(self) -> list[Item]:
        items = await self.repo.list_items()
        return [item for item in items if item.is_below_reorder_point]
