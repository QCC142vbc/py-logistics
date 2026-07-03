from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class ShipmentCreate(BaseModel):
    order_id: str
    origin: dict
    destination: dict
    items: list[dict]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shipment(request: ShipmentCreate):
    """Create a new shipment."""
    return {
        "shipment_id": "ship-123",
        "tracking_number": "TRK-123456",
        "estimated_arrival": "2024-01-20T00:00:00",
    }


@router.get("/{shipment_id}/track")
async def track_shipment(shipment_id: str):
    """Track a shipment."""
    return {
        "shipment_id": shipment_id,
        "status": "in_transit",
        "current_location": {"latitude": 41.8781, "longitude": -87.6298},
        "estimated_arrival": "2024-01-20T00:00:00",
    }


@router.get("/{shipment_id}")
async def get_shipment(shipment_id: str):
    """Get shipment details."""
    return {
        "id": shipment_id,
        "order_id": "ord-123",
        "tracking_number": "TRK-123456",
        "status": "in_transit",
    }
