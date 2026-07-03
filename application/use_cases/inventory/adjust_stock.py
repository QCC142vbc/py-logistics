from dataclasses import dataclass

from src.domain.inventory.models import StockLevel
from src.domain.inventory.services import InventoryService


@dataclass
class AdjustStockRequest:
    item_id: str
    quantity: int
    reason: str
    performed_by: str = None


@dataclass
class AdjustStockResponse:
    item_id: str
    new_quantity: int
    transaction_id: str


class AdjustStockUseCase:
    def __init__(self, inventory_service: InventoryService) -> None:
        self._inventory_service = inventory_service

    async def execute(self, request: AdjustStockRequest) -> AdjustStockResponse:
        stock_level = await self._inventory_service.adjust_stock(
            item_id=request.item_id,
            quantity=request.quantity,
            reason=request.reason,
            performed_by=request.performed_by,
        )

        return AdjustStockResponse(
            item_id=request.item_id,
            new_quantity=stock_level.available,
            transaction_id=f"ADJUST-{request.item_id}",
        )
