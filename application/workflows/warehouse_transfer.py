from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.application.use_cases.transportation.create_shipment import (
    CreateShipmentRequest,
    CreateShipmentUseCase,
)
from src.application.use_cases.warehouse.initiate_transfer import (
    InitiateTransferRequest,
    InitiateTransferUseCase,
    TransferItemRequest,
)
from src.application.dto.common import LocationDTO
from src.application.use_cases.transportation.create_shipment import (
    ShipmentItemRequest,
    ShipmentRequirementsDTO,
)


@dataclass
class TransferItemRequest:
    item_id: str
    quantity: int
    sku: str = None


@dataclass
class WarehouseTransferRequest:
    from_warehouse_id: str
    to_warehouse_id: str
    items: List[TransferItemRequest]


@dataclass
class WarehouseTransferResponse:
    transfer_id: str
    shipment_id: str
    estimated_arrival: datetime


class WarehouseTransferWorkflow:
    def __init__(
        self,
        warehouse_transfer: InitiateTransferUseCase,
        transportation_service,
        create_shipment: CreateShipmentUseCase,
    ) -> None:
        self._warehouse_transfer = warehouse_transfer
        self._transportation_service = transportation_service
        self._create_shipment = create_shipment

    async def execute(self, request: WarehouseTransferRequest) -> WarehouseTransferResponse:
        # Step 1: Initiate warehouse transfer
        transfer_request = InitiateTransferRequest(
            from_warehouse_id=request.from_warehouse_id,
            to_warehouse_id=request.to_warehouse_id,
            items=[
                TransferItemRequest(
                    item_id=item.item_id,
                    quantity=item.quantity,
                    sku=item.sku,
                )
                for item in request.items
            ],
            initiated_by="system",
        )
        transfer_response = await self._warehouse_transfer.execute(transfer_request)

        # Step 2: Create shipment for the transfer
        shipment_request = CreateShipmentRequest(
            order_id=transfer_response.transfer_id,
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

        return WarehouseTransferResponse(
            transfer_id=transfer_response.transfer_id,
            shipment_id=shipment_response.shipment_id,
            estimated_delivery=datetime.fromisoformat(shipment_response.estimated_arrival),
        )
