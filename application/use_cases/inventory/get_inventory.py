from dataclasses import dataclass
from typing import List, Optional

from src.application.dto.inventory import ItemDTO
from src.domain.inventory.models import Item
from src.domain.inventory.repository import ItemFilter
from src.domain.inventory.services import InventoryService


@dataclass
class GetInventoryRequest:
    filter: Optional[ItemFilter] = None


@dataclass
class GetInventoryResponse:
    items: List[ItemDTO]
    total: int


class GetInventoryUseCase:
    def __init__(self, inventory_service: InventoryService) -> None:
        self._inventory_service = inventory_service

    async def execute(self, request: GetInventoryRequest) -> GetInventoryResponse:
        items = await self._inventory_service.list_items(request.filter)

        item_dtos = [
            ItemDTO(
                id=item.id,
                sku=item.sku,
                name=item.name,
                quantity=item.quantity,
                unit_cost=str(item.unit_cost),
                location=item.location,
                category=item.category,
            )
            for item in items
        ]

        return GetInventoryResponse(
            items=item_dtos,
            total=len(item_dtos),
        )
