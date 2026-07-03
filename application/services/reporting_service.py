from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.analytics.reporting.report_generator import ReportGenerator


@dataclass
class ReportFilter:
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    category: Optional[str] = None


@dataclass
class Report:
    id: str
    title: str
    generated_at: datetime
    data: dict


class ReportingService:
    def __init__(self, analytics_engine) -> None:
        self._analytics_engine = analytics_engine

    async def generate_inventory_report(self, filter: ReportFilter) -> Report:
        """Generate inventory report."""
        data = await self._analytics_engine.generate_inventory_metrics(filter)
        return Report(
            id=f"INV-{datetime.utcnow().timestamp()}",
            title="Inventory Report",
            generated_at=datetime.utcnow(),
            data=data,
        )

    async def generate_order_report(self, filter: ReportFilter) -> Report:
        """Generate order report."""
        data = await self._analytics_engine.generate_order_metrics(filter)
        return Report(
            id=f"ORD-{datetime.utcnow().timestamp()}",
            title="Order Report",
            generated_at=datetime.utcnow(),
            data=data,
        )

    async def generate_supplier_performance_report(
        self,
        supplier_id: str,
        date_range,
    ) -> Report:
        """Generate supplier performance report."""
        data = await self._analytics_engine.generate_supplier_metrics(supplier_id, date_range)
        return Report(
            id=f"SUP-{supplier_id}-{datetime.utcnow().timestamp()}",
            title=f"Supplier Performance Report - {supplier_id}",
            generated_at=datetime.utcnow(),
            data=data,
        )
