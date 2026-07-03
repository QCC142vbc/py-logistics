from dataclasses import dataclass

from src.application.dto.order import OrderDTO
from src.domain.order.models import Order
from src.domain.order.services import OrderService


@dataclass
class GetOrderRequest:
    order_id: str


@dataclass
class GetOrderResponse:
    order: OrderDTO


class GetOrderuseCase:
    def __init__(self, order_service: OrderService) -> None:
        self._order_service = order_service

    async def execute(self, request: GetOrderRequest) -> GetOrderResponse:
        order = await self._order_service.get_order(request.order_id)

        order_dto = OrderDTO(
            id=order.id,
            customer_id=order.customer_id,
            order_date=order.order_date.isoformat() if order.order_date else None,
            status=order.status.value,
            items=[
                {
                    "item_id": item.item_id,
                    "sku": item.sku,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "subtotal": str(item.subtotal),
                }
                for item in order.items
            ],
            total_amount=str(order.total_amount),
        )

        return GetOrderResponse(order=order_dto)
