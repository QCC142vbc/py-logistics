from typing import Optional
from src.models.order import Order, OrderStatus
from src.repositories.repository import Repository
from src.services.inventory_service import InventoryService


class OrderService:
    def __init__(self, repo: Repository, inventory_service: InventoryService):
        self.repo = repo
        self.inventory_service = inventory_service

    async def create_order(self, order: Order) -> Order:
        if not order.items:
            raise ValueError("Order must have at least one item")
        
        # Validate items exist and have sufficient stock
        for item in order.items:
            inventory_item = await self.inventory_service.get_item(item.item_id)
            if not inventory_item:
                raise ValueError(f"Item {item.item_id} not found")
            if inventory_item.quantity < item.quantity:
                raise ValueError(f"Insufficient stock for item {item.sku}")
        
        # Calculate total
        order.calculate_total()
        
        # Create order
        order_id = await self.repo.create_order(order)
        order.id = order_id
        
        # Reserve stock (simplified - in real system, use transactions)
        for item in order.items:
            await self.inventory_service.adjust_stock(item.item_id, -item.quantity)
        
        return order

    async def get_order(self, order_id: str) -> Optional[Order]:
        return await self.repo.get_order(order_id)

    async def list_orders(self) -> list[Order]:
        return await self.repo.list_orders()

    async def process_order(self, order_id: str) -> Optional[Order]:
        order = await self.repo.get_order(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if order.status != OrderStatus.PENDING:
            raise ValueError("Order can only be processed from PENDING status")
        
        order = await self.repo.update_order_status(order_id, OrderStatus.PROCESSING)
        return order

    async def cancel_order(self, order_id: str) -> Optional[Order]:
        order = await self.repo.get_order(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if not order.can_be_cancelled:
            raise ValueError("Order cannot be cancelled in current status")
        
        # Restore stock
        for item in order.items:
            await self.inventory_service.adjust_stock(item.item_id, item.quantity)
        
        order = await self.repo.update_order_status(order_id, OrderStatus.CANCELLED)
        return order
