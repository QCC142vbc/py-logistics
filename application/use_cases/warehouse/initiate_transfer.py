from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.domain.warehouse.models import TransferItem, WarehouseTransfer, TransferStatus
from src.domain.warehouse.services import WarehouseService


@dataclass
class TransferItemRequest:
    item_id: str
    quantity: int
    sku: str = None


@dataclass
class InitiateTransferRequest:
    from_warehouse_id: str
    to_warehouse_id: str
    items: List[TransferItemRequest]
    initiated_by: str
    notes: str = None


@dataclass
class InitiateTransferResponse:
    transfer_id: str
    status: TransferStatus


class InitiateTransferUseCase:
    def __init__(self, warehouse_service: WarehouseService) -> None:
        self._warehouse_service = warehouse_service

    async def execute(self, request: InitiateTransferRequest) -> InitiateTransferResponse:
        transfer_items = [
            TransferItem(
                item_id=item.item_id,
                quantity=item.quantity,
                sku=item.sku,
            )
            for item in request.items
        ]

        transfer = WarehouseTransfer(
            id=None,
            from_warehouse_id=request.from_warehouse_id,
            to_warehouse_id=request.to_warehouse_id,
            items=transfer_items,
            status=TransferStatus.PENDING,
            initiated_by=request.initiated_by,
            initiated_at=datetime.utcnow(),
            notes=request.notes,
        )

        created_transfer = await self._warehouse_service.initiate_transfer(transfer)

        return InitiateTransferResponse(
            transfer_id=created_transfer.id,
            status=created_transfer.status,
        )
