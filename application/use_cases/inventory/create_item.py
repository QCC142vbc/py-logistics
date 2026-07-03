from dataclasses import dataclass
from decimal import Decimal

from src.domain.inventory.models import Item
from src.domain.inventory.services import InventoryService


@dataclass
class CreateItemRequest:
    sku: str
    name: str
    quantity: int
    unit_cost: Decimal
    location: str
    category: str
    reorder_point: int
    lead_time_days: int
    description: str = None
    weight_kg: float = None
    volume_m3: float = None
    supplier_id: str = None


@dataclass
class CreateItemResponse:
    item_id: str
    sku: str
    status: str


class CreateItemUseCase:
    def __init__(self, inventory_service: InventoryService) -> None:
        self._inventory_service = inventory_service

    async def execute(self, request: CreateItemRequest) -> CreateItemResponse:
        item = Item(
            id=None,
            sku=request.sku,
            name=request.name,
            quantity=request.quantity,
            unit_cost=request.unit_cost,
            location=request.location,
            category=request.category,
            reorder_point=request.reorder_point,
            lead_time_days=request.lead_time_days,
            description=request.description,
            weight_kg=request.weight_kg,
            volume_m3=request.volume_m3,
            supplier_id=request.supplier_id,
        )

        created_item = await self._inventory_service.add_item(item)

        return CreateItemResponse(
            item_id=created_item.id,
            sku=created_item.sku,
            status="created",
        )
