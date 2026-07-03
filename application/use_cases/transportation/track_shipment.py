from dataclasses import dataclass

from src.application.dto.common import LocationDTO
from src.application.dto.transportation import TrackShipmentResponse
from src.domain.transportation.models import Shipment, ShipmentStatus
from src.domain.transportation.services import TransportationService


@dataclass
class TrackShipmentRequest:
    shipment_id: str


class TrackShipmentUseCase:
    def __init__(self, transportation_service: TransportationService) -> None:
        self._transportation_service = transportation_service

    async def execute(self, request: TrackShipmentRequest) -> TrackShipmentResponse:
        shipment = await self._transportation_service.get_shipment(request.shipment_id)

        current_location_dto = None
        if shipment.current_location:
            current_location_dto = LocationDTO(
                latitude=shipment.current_location.latitude,
                longitude=shipment.current_location.longitude,
                address=shipment.current_location.address,
            )

        return TrackShipmentResponse(
            shipment_id=shipment.id,
            status=shipment.status.value,
            current_location=current_location_dto,
            estimated_arrival=shipment.estimated_arrival.isoformat(),
        )
