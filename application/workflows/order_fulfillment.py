from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from src.application.use_cases.order.create_order import CreateOrderUseCase, CreateOrderRequest
from src.application.use_cases.order.process_order import ProcessOrderUseCase, ProcessOrderRequest
from src.application.use_cases.transportation.create_shipment import (
    CreateShipmentRequest,
    CreateShipmentUseCase,
)
from src.application.dto.common import AddressDTO


@dataclass
class OrderItemRequest:
    item_id: str
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class OrderFulfillmentRequest:
    customer_id: str
    items: List[OrderItemRequest]
    shipping_address: AddressDTO
    billing_address: AddressDTO


@dataclass
class OrderFulfillmentResponse:
    order_id: str
    shipment_id: str
    estimated_delivery: datetime


class OrderFulfillmentWorkflow:
    def __init__(
        self,
        create_order: CreateOrderUseCase,
        process_order: ProcessOrderUseCase,
        create_shipment: CreateShipmentUseCase,
    ) -> None:
        self._create_order = create_order
        self._process_order = process_order
        self._create_shipment = create_shipment

    async def execute(self, request: OrderFulfillmentRequest) -> OrderFulfillmentResponse:
        # Step 1: Create the order
        create_order_request = CreateOrderRequest(
            customer_id=request.customer_id,
            items=[
                {
                    "item_id": item.item_id,
                    "sku": item.sku,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                }
                for item in request.items
            ],
            shipping_address=request.shipping_address,
            billing_address=request.billing_address,
        )
        order_response = await self._create_order.execute(create_order_request)

        # Step 2: Process the order (reserve stock)
        process_request = ProcessOrderRequest(order_id=order_response.order_id)
        await self._process_order.execute(process_request)

        # Step 3: Create shipment (simplified - in real implementation would get route)
        from src.application.dto.common import LocationDTO
        from src.application.use_cases.transportation.create_shipment import (
            ShipmentItemRequest,
            ShipmentRequirementsDTO,
        )

        shipment_request = CreateShipmentRequest(
            order_id=order_response.order_id,
            origin=LocationDTO(latitude=0, longitude=0),
            destination=LocationDTO(latitude=0, longitude=0),
            items=[
                ShipmentItemRequest(
                    item_id=item.item_id,
                    quantity=item.quantity,
                    weight_kg=1.0,
                )
                for item in request.items
            ],
            requirements=ShipmentRequirementsDTO(weight_kg=10.0, volume_m3=1.0),
        )
        shipment_response = await self._create_shipment.execute(shipment_request)

        return OrderFulfillmentResponse(
            order_id=order_response.order_id,
            shipment_id=shipment_response.shipment_id,
            estimated_delivery=datetime.fromisoformat(shipment_response.estimated_arrival),
        )
