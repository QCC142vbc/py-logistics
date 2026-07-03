from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.domain.order.services import OrderService


@dataclass
class CancelOrderRequest:
    order_id: str
    reason: str


@dataclass
class CancelOrderResponse:
    success: bool
    refund_amount: Optional[Decimal]


class CancelOrderUseCase:
    def __init__(self, order_service: OrderService) -> None:
        self._order_service = order_service

    async def execute(self, request: CancelOrderRequest) -> CancelOrderResponse:
        order = await self._order_service.get_order(request.order_id)
        success = await self._order_service.cancel_order(request.order_id, request.reason)

        # In a real implementation, this would process a refund
        refund_amount = order.total_amount if success else None

        return CancelOrderResponse(
            success=success,
            refund_amount=refund_amount,
        )
