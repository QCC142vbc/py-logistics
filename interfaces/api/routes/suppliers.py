from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class SupplierCreate(BaseModel):
    name: str
    contact_email: str
    phone: str
    address: dict
    payment_terms: str
    lead_time_days: int


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_supplier(request: SupplierCreate):
    """Register a new supplier."""
    return {"id": "sup-123", "name": request.name, "status": "registered"}


@router.get("/")
async def list_suppliers():
    """List all suppliers."""
    return {
        "suppliers": [
            {"id": "sup-001", "name": "Acme Supplies", "rating": 4.5, "active": True},
            {"id": "sup-002", "name": "Global Logistics", "rating": 4.2, "active": True},
        ],
        "total": 2,
    }


@router.get("/{supplier_id}")
async def get_supplier(supplier_id: str):
    """Get a specific supplier."""
    return {
        "id": supplier_id,
        "name": "Acme Supplies",
        "contact_email": "contact@acme.com",
        "rating": 4.5,
        "active": True,
    }


@router.get("/{supplier_id}/score")
async def evaluate_supplier(supplier_id: str):
    """Evaluate supplier performance."""
    return {
        "supplier_id": supplier_id,
        "reliability_score": 85.0,
        "quality_score": 90.0,
        "cost_score": 75.0,
        "overall_score": 84.5,
    }
