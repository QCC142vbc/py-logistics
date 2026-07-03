from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class LeadTimeDistribution:
    mean: float
    std_dev: float
    min_days: int
    max_days: int


@dataclass
class LeadTimeForecast:
    supplier_id: str
    item_category: str
    expected_days: int
    confidence: float
    distribution: LeadTimeDistribution


class LeadTimeForecaster:
    """Forecasts supplier lead times."""

    def forecast_lead_time(
        self,
        supplier_id: str,
        item_category: str,
    ) -> LeadTimeForecast:
        """Forecast lead time for a supplier and item category."""
        # Simplified implementation
        return LeadTimeForecast(
            supplier_id=supplier_id,
            item_category=item_category,
            expected_days=7,
            confidence=0.85,
            distribution=LeadTimeDistribution(
                mean=7.0,
                std_dev=2.0,
                min_days=3,
                max_days=14,
            ),
        )
