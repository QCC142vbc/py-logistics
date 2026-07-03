from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class OrderCreate(BaseModel):
    customer_id: str
    items: list[dict]
    shipping_address: dict
    billing_address: dict


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(request: OrderCreate):
    """Create a new order."""
    return {"id": "ord-123", "customer_id": request.customer_id, "status": "pending"}


@router.get("/{order_id}")
async def get_order(order_id: str):
    """Get a specific order."""
    return {
        "id": order_id,
        "customer_id": "cust-001",
        "status": "processing",
        "total_amount": "250.00",
    }


@router.post("/{order_id}/process")
async def process_order(order_id: str):
    """Process an order."""
    return {"order_id": order_id, "status": "processing", "shipment_id": "ship-123"}


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: str, reason: str = None):
    """Cancel an order."""
    return {"order_id": order_id, "status": "cancelled", "refund_amount": "250.00"}


@router.get("/")
async def list_orders(customer_id: str = None, status: str = None):
    """List orders."""
    return {
        "orders": [
            {"id": "ord-001", "customer_id": "cust-001", "status": "delivered"},
            {"id": "ord-002", "customer_id": "cust-002", "status": "shipped"},
        ],
        "total": 2,
    }
