from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class WarehouseCreate(BaseModel):
    name: str
    location: dict
    capacity_sqm: float
    manager_id: str
    operating_hours: dict


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_warehouse(request: WarehouseCreate):
    """Register a new warehouse."""
    return {"id": "wh-123", "name": request.name, "status": "registered"}


@router.get("/")
async def list_warehouses():
    """List all warehouses."""
    return {
        "warehouses": [
            {"id": "wh-001", "name": "Main Distribution Center", "utilization": 35.0},
            {"id": "wh-002", "name": "West Coast Fulfillment", "utilization": 52.5},
        ],
        "total": 2,
    }


@router.get("/{warehouse_id}/utilization")
async def get_utilization(warehouse_id: str):
    """Get warehouse utilization."""
    return {
        "warehouse_id": warehouse_id,
        "utilization_percentage": 35.0,
        "available_capacity_sqm": 6500.0,
    }
