from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class RealTimeMetrics:
    pending_orders: int
    in_transit_shipments: int
    low_stock_items: int
    system_health: str


@dataclass
class TrendData:
    metric: str
    values: List[float]
    timestamps: List[datetime]


class DashboardMetrics:
    """Provides dashboard metrics and trends."""

    def get_real_time_metrics(self) -> RealTimeMetrics:
        """Get current real-time metrics."""
        return RealTimeMetrics(
            pending_orders=25,
            in_transit_shipments=45,
            low_stock_items=12,
            system_health="healthy",
        )

    def get_historical_trends(
        self,
        metric: str,
        period,
    ) -> TrendData:
        """Get historical trend data for a metric."""
        # Simplified implementation
        import random
        from datetime import timedelta

        values = [random.uniform(80, 100) for _ in range(30)]
        timestamps = [
            datetime.utcnow() - timedelta(days=i) for i in range(30)
        ]
        timestamps.reverse()

        return TrendData(
            metric=metric,
            values=values,
            timestamps=timestamps,
        )
