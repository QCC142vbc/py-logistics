from dataclasses import dataclass

from src.domain.inventory.services import InventoryService
from src.domain.order.services import OrderService
from src.domain.transportation.services import TransportationService


@dataclass
class ProcessOrderRequest:
    order_id: str


@dataclass
class ProcessOrderResponse:
    success: bool
    shipment_id: str = None


class ProcessOrderUseCase:
    def __init__(
        self,
        order_service: OrderService,
        inventory_service: InventoryService,
        transportation_service: TransportationService,
    ) -> None:
        self._order_service = order_service
        self._inventory_service = inventory_service
        self._transportation_service = transportation_service

    async def execute(self, request: ProcessOrderRequest) -> ProcessOrderResponse:
        # Process the order (reserve stock, create shipment, etc.)
        success = await self._order_service.process_order(request.order_id)

        # In a real implementation, this would also create a shipment
        # For now, return success without shipment
        return ProcessOrderResponse(
            success=success,
            shipment_id=None,
        )
