from fastapi import APIRouter

router = APIRouter()


@router.get("/inventory/turnover")
async def get_inventory_turnover():
    """Get inventory turnover metrics."""
    return {
        "turnover_rate": 4.5,
        "days_sales_of_inventory": 81,
        "period": "last_30_days",
    }


@router.get("/supplier/performance")
async def get_supplier_performance(supplier_id: str = None):
    """Get supplier performance metrics."""
    return {
        "supplier_id": supplier_id or "all",
        "on_time_delivery_rate": 92.5,
        "quality_acceptance_rate": 95.0,
        "average_lead_time_days": 7,
    }


@router.get("/risk/assessment")
async def get_risk_assessment():
    """Get risk assessment report."""
    return {
        "overall_risk_level": "medium",
        "supplier_risks": [
            {"supplier_id": "sup-001", "risk_level": "low", "score": 15.0},
            {"supplier_id": "sup-002", "risk_level": "medium", "score": 45.0},
        ],
        "inventory_risks": [
            {"item_id": "item-001", "risk_level": "low", "score": 10.0},
        ],
    }
