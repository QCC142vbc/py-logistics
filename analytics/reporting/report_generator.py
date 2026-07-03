from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class ReportFormat(Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"


@dataclass
class ReportFilter:
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    category: Optional[str] = None
    location: Optional[str] = None


@dataclass
class Report:
    id: str
    title: str
    generated_at: datetime
    format: ReportFormat
    data: dict
    file_path: Optional[str] = None


@dataclass
class OrderPerformanceReport:
    total_orders: int
    fulfilled_orders: int
    fulfillment_rate: float
    average_order_value: Decimal
    total_revenue: Decimal


@dataclass
class SupplierScorecard:
    supplier_id: str
    supplier_name: str
    overall_score: float
    reliability_score: float
    quality_score: float
    cost_score: float
    delivery_score: float
    period: str


@dataclass
class DashboardMetrics:
    pending_orders: int
    in_transit_shipments: int
    low_stock_items: int
    system_health: str
    total_inventory_value: Decimal
    monthly_revenue: Decimal


class ReportGenerator:
    """Generates various reports for the logistics system."""

    def generate_inventory_report(
        self,
        filter: ReportFilter,
        format: ReportFormat = ReportFormat.PDF,
    ) -> Report:
        """Generate inventory report."""
        # In a real implementation, this would query data and generate reports
        data = {
            "total_items": 150,
            "total_value": "125000.00",
            "low_stock_items": 12,
            "categories": {
                "widgets": 50,
                "components": 45,
                "electronics": 55,
            },
        }

        return Report(
            id=f"INV-{datetime.utcnow().timestamp()}",
            title="Inventory Report",
            generated_at=datetime.utcnow(),
            format=format,
            data=data,
        )

    def generate_order_performance_report(
        self,
        date_range,
    ) -> OrderPerformanceReport:
        """Generate order performance report."""
        # Simplified implementation
        return OrderPerformanceReport(
            total_orders=500,
            fulfilled_orders=475,
            fulfillment_rate=0.95,
            average_order_value=Decimal("250.00"),
            total_revenue=Decimal("125000.00"),
        )

    def generate_supplier_scorecard(
        self,
        supplier_id: str,
        period,
    ) -> SupplierScorecard:
        """Generate supplier performance scorecard."""
        return SupplierScorecard(
            supplier_id=supplier_id,
            supplier_name="Acme Supplies Inc",
            overall_score=84.5,
            reliability_score=85.0,
            quality_score=90.0,
            cost_score=75.0,
            delivery_score=88.0,
            period="last_30_days",
        )

    def generate_dashboard_metrics(
        self,
        date_range,
    ) -> DashboardMetrics:
        """Generate dashboard metrics."""
        return DashboardMetrics(
            pending_orders=25,
            in_transit_shipments=45,
            low_stock_items=12,
            system_health="healthy",
            total_inventory_value=Decimal("125000.00"),
            monthly_revenue=Decimal("375000.00"),
        )
