from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.application.use_cases.inventory.create_item import CreateItemRequest, CreateItemUseCase
from src.application.use_cases.inventory.adjust_stock import AdjustStockRequest, AdjustStockUseCase
from src.application.use_cases.inventory.get_inventory import GetInventoryRequest, GetInventoryUseCase

router = APIRouter()


class ItemCreate(BaseModel):
    sku: str
    name: str
    quantity: int
    unit_cost: float
    location: str
    category: str
    reorder_point: int
    lead_time_days: int


class StockAdjustment(BaseModel):
    quantity: int
    reason: str


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(request: ItemCreate):
    """Create a new inventory item."""
    # In a real implementation, this would use dependency injection
    # use_case = CreateItemUseCase(inventory_service)
    # response = await use_case.execute(...)
    return {"id": "item-123", "sku": request.sku, "status": "created"}


@router.get("/items")
async def list_items():
    """List all inventory items."""
    # use_case = GetInventoryUseCase(inventory_service)
    # response = await use_case.execute(...)
    return {
        "items": [
            {"id": "item-001", "sku": "ITEM-001", "name": "Widget A", "quantity": 100},
            {"id": "item-002", "sku": "ITEM-002", "name": "Component B", "quantity": 50},
        ],
        "total": 2,
    }


@router.patch("/items/{item_id}/stock")
async def adjust_stock(item_id: str, request: StockAdjustment):
    """Adjust stock level for an item."""
    # use_case = AdjustStockUseCase(inventory_service)
    # response = await use_case.execute(...)
    return {"item_id": item_id, "new_quantity": 100 + request.quantity}


@router.get("/items/{item_id}")
async def get_item(item_id: str):
    """Get a specific item."""
    return {"id": item_id, "sku": "ITEM-001", "name": "Widget A", "quantity": 100}


@router.get("/items/low-stock")
async def get_low_stock_items():
    """Get items with low stock."""
    return {
        "items": [
            {"id": "item-002", "sku": "ITEM-002", "quantity": 5, "reorder_point": 10},
        ],
        "total": 1,
    }
