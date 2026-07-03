from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List


@dataclass
class DeliveryRecord:
    supplier_id: str
    delivery_date: datetime
    on_time: bool
    quantity_delivered: int
    quantity_ordered: int
    damaged_items: int = 0


@dataclass
class QualityRecord:
    supplier_id: str
    inspection_date: datetime
    pass_rate: float
    total_inspected: int
    defects_found: int


class ScoreCalculator:
    """Calculates various performance scores for suppliers."""

    def __init__(self) -> None:
        # In a real implementation, these would fetch data from repositories
        self._delivery_records: List[DeliveryRecord] = []
        self._quality_records: List[QualityRecord] = []

    def calculate_reliability(self, supplier_id: str) -> float:
        """
        Calculate reliability score based on delivery history.
        Score is 0-100.
        """
        # Get delivery records for the supplier
        records = [r for r in self._delivery_records if r.supplier_id == supplier_id]
        
        if not records:
            return 50.0  # Default score for new suppliers

        # Calculate on-time delivery rate
        on_time_deliveries = sum(1 for r in records if r.on_time)
        on_time_rate = on_time_deliveries / len(records)

        # Calculate fill rate (quantity delivered / quantity ordered)
        total_ordered = sum(r.quantity_ordered for r in records)
        total_delivered = sum(r.quantity_delivered for r in records)
        fill_rate = total_delivered / total_ordered if total_ordered > 0 else 0

        # Calculate damage rate
        total_delivered_items = sum(r.quantity_delivered for r in records)
        total_damaged = sum(r.damaged_items for r in records)
        damage_rate = total_damaged / total_delivered_items if total_delivered_items > 0 else 0

        # Combine into reliability score
        reliability_score = (
            on_time_rate * 0.5
            + fill_rate * 0.4
            + (1 - damage_rate) * 0.1
        ) * 100

        return min(100.0, max(0.0, reliability_score))

    def calculate_quality(self, supplier_id: str) -> float:
        """
        Calculate quality score based on inspection records.
        Score is 0-100.
        """
        records = [r for r in self._quality_records if r.supplier_id == supplier_id]
        
        if not records:
            return 50.0

        # Average pass rate across all inspections
        avg_pass_rate = sum(r.pass_rate for r in records) / len(records)

        return avg_pass_rate

    def calculate_cost(
        self,
        supplier_id: str,
        prices: List[Decimal],
        market_average: Decimal,
    ) -> float:
        """
        Calculate cost score based on price competitiveness.
        Score is 0-100, where 100 is most competitive.
        """
        if not prices:
            return 50.0

        avg_price = sum(prices) / len(prices)
        
        if market_average == 0:
            return 50.0

        # Score based on how much cheaper than market average
        price_ratio = avg_price / market_average
        
        if price_ratio <= 0.8:
            return 100.0
        elif price_ratio <= 0.9:
            return 90.0
        elif price_ratio <= 1.0:
            return 80.0
        elif price_ratio <= 1.1:
            return 60.0
        elif price_ratio <= 1.2:
            return 40.0
        else:
            return 20.0

    def calculate_delivery(
        self,
        supplier_id: str,
        on_time_deliveries: int,
        total_deliveries: int,
    ) -> float:
        """
        Calculate delivery score based on on-time performance.
        Score is 0-100.
        """
        if total_deliveries == 0:
            return 50.0

        on_time_rate = on_time_deliveries / total_deliveries
        return on_time_rate * 100

    def add_delivery_record(self, record: DeliveryRecord) -> None:
        """Add a delivery record for scoring calculations."""
        self._delivery_records.append(record)

    def add_quality_record(self, record: QualityRecord) -> None:
        """Add a quality record for scoring calculations."""
        self._quality_records.append(record)
