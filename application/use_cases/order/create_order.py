from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.application.dto.common import AddressDTO
from src.application.dto.order import OrderDTO
from src.domain.inventory.services import InventoryService
from src.domain.order.models import Order, OrderItem, OrderStatus
from src.domain.order.services import OrderService
from src.domain.supplier.models import Address


@dataclass
class OrderItemRequest:
    item_id: str
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class CreateOrderRequest:
    customer_id: str
    items: List[OrderItemRequest]
    shipping_address: AddressDTO
    billing_address: AddressDTO
    customer_name: str = None
    customer_email: str = None
    customer_phone: str = None


@dataclass
class CreateOrderResponse:
    order_id: str
    status: OrderStatus
    total_amount: Decimal


class CreateOrderUseCase:
    def __init__(
        self,
        order_service: OrderService,
        inventory_service: InventoryService,
    ) -> None:
        self._order_service = order_service
        self._inventory_service = inventory_service

    async def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        # Convert DTOs to domain models
        shipping_address = Address(
            street=request.shipping_address.street,
            city=request.shipping_address.city,
            state=request.shipping_address.state,
            postal_code=request.shipping_address.postal_code,
            country=request.shipping_address.country,
            address_line2=request.shipping_address.address_line2,
        )

        billing_address = Address(
            street=request.billing_address.street,
            city=request.billing_address.city,
            state=request.billing_address.state,
            postal_code=request.billing_address.postal_code,
            country=request.billing_address.country,
            address_line2=request.billing_address.address_line2,
        )

        order_items = [
            OrderItem(
                item_id=item.item_id,
                sku=item.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in request.items
        ]

        total_amount = sum(item.subtotal for item in order_items)

        order = Order(
            id=None,
            customer_id=request.customer_id,
            order_date=None,
            status=OrderStatus.PENDING,
            items=order_items,
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address,
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            customer_phone=request.customer_phone,
        )

        created_order = await self._order_service.create_order(order)

        return CreateOrderResponse(
            order_id=created_order.id,
            status=created_order.status,
            total_amount=created_order.total_amount,
        )
