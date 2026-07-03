from dataclasses import dataclass
from typing import List

from src.application.dto.common import LocationDTO
from src.application.dto.transportation import ShipmentDTO
from src.domain.common.models import Location
from src.domain.transportation.models import Shipment, ShipmentItem, ShipmentStatus
from src.domain.transportation.services import TransportationService


@dataclass
class ShipmentItemRequest:
    item_id: str
    quantity: int
    weight_kg: float
    volume_m3: float = None


@dataclass
class ShipmentRequirementsDTO:
    weight_kg: float
    volume_m3: float
    priority: str = "standard"
    special_handling: bool = False
    temperature_controlled: bool = False
    hazardous: bool = False


@dataclass
class CreateShipmentRequest:
    order_id: str
    origin: LocationDTO
    destination: LocationDTO
    items: List[ShipmentItemRequest]
    requirements: ShipmentRequirementsDTO


@dataclass
class CreateShipmentResponse:
    shipment_id: str
    tracking_number: str
    estimated_arrival: str


class CreateShipmentUseCase:
    def __init__(self, transportation_service: TransportationService) -> None:
        self._transportation_service = transportation_service

    async def execute(self, request: CreateShipmentRequest) -> CreateShipmentResponse:
        origin = Location(
            latitude=request.origin.latitude,
            longitude=request.origin.longitude,
            address=request.origin.address,
        )

        destination = Location(
            latitude=request.destination.latitude,
            longitude=request.destination.longitude,
            address=request.destination.address,
        )

        shipment_items = [
            ShipmentItem(
                shipment_id="",
                item_id=item.item_id,
                quantity=item.quantity,
                weight_kg=item.weight_kg,
                volume_m3=item.volume_m3,
            )
            for item in request.items
        ]

        # In a real implementation, this would plan a route and select a carrier
        # For now, create a simplified shipment
        from datetime import datetime, timedelta

        shipment = Shipment(
            id=None,
            order_id=request.order_id,
            route_id="",
            carrier="default_carrier",
            tracking_number=f"TRK-{request.order_id}",
            status=ShipmentStatus.PENDING,
            estimated_arrival=datetime.utcnow() + timedelta(days=3),
            items=shipment_items,
        )

        created_shipment = await self._transportation_service.create_shipment(shipment)

        return CreateShipmentResponse(
            shipment_id=created_shipment.id,
            tracking_number=created_shipment.tracking_number,
            estimated_arrival=created_shipment.estimated_arrival.isoformat(),
        )
