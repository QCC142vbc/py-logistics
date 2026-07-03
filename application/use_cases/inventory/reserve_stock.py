from dataclasses import dataclass

from src.domain.inventory.services import InventoryService


@dataclass
class ReserveStockRequest:
    item_id: str
    quantity: int
    order_id: str


@dataclass
class ReserveStockResponse:
    success: bool
    reserved_quantity: int


class ReserveStockUseCase:
    def __init__(self, inventory_service: InventoryService) -> None:
        self._inventory_service = inventory_service

    async def execute(self, request: ReserveStockRequest) -> ReserveStockResponse:
        success = await self._inventory_service.reserve_stock(
            item_id=request.item_id,
            quantity=request.quantity,
            order_id=request.order_id,
        )

        return ReserveStockResponse(
            success=success,
            reserved_quantity=request.quantity if success else 0,
        )
