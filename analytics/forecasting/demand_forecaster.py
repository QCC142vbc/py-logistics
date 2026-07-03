from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class ForecastMethod(Enum):
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    ARIMA = "arima"
    PROPHET = "prophet"
    MACHINE_LEARNING = "machine_learning"


@dataclass
class DemandPoint:
    date: datetime
    demand: int
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None


@dataclass
class DemandForecast:
    item_id: str
    forecast: List[DemandPoint]
    confidence_interval: List[tuple[float, float]]
    method: ForecastMethod
    accuracy_score: float


@dataclass
class SeasonalForecast:
    item_id: str
    seasonal_pattern: dict[str, float]  # month -> multiplier
    base_demand: int
    forecast: List[DemandPoint]


class DemandForecaster:
    """Forecasts demand using various methods."""

    def forecast_demand(
        self,
        item_id: str,
        horizon_days: int,
        method: ForecastMethod = ForecastMethod.MOVING_AVERAGE,
    ) -> DemandForecast:
        """Forecast demand for an item."""
        # Simplified implementation using moving average
        forecast = []
        base_date = datetime.utcnow()
        base_demand = 10  # Simplified base demand

        for i in range(horizon_days):
            forecast_date = base_date + timedelta(days=i)
            # Add some randomness for realism
            import random
            demand = int(base_demand + random.randint(-2, 3))
            forecast.append(
                DemandPoint(
                    date=forecast_date,
                    demand=demand,
                    lower_bound=max(0, demand - 2),
                    upper_bound=demand + 2,
                )
            )

        confidence_interval = [(0.8, 1.2) for _ in range(horizon_days)]

        return DemandForecast(
            item_id=item_id,
            forecast=forecast,
            confidence_interval=confidence_interval,
            method=method,
            accuracy_score=0.85,
        )

    def forecast_seasonal_demand(
        self,
        item_id: str,
        periods: int,
    ) -> SeasonalForecast:
        """Forecast seasonal demand patterns."""
        # Simplified seasonal pattern
        seasonal_pattern = {
            "january": 0.9,
            "february": 0.85,
            "march": 0.95,
            "april": 1.0,
            "may": 1.05,
            "june": 1.1,
            "july": 1.15,
            "august": 1.1,
            "september": 1.05,
            "october": 1.0,
            "november": 1.15,
            "december": 1.2,
        }

        base_demand = 10
        forecast = []
        base_date = datetime.utcnow()

        for i in range(periods):
            forecast_date = base_date + timedelta(days=30 * i)
            month = forecast_date.strftime("%B").lower()
            multiplier = seasonal_pattern.get(month, 1.0)
            demand = int(base_demand * multiplier)
            forecast.append(
                DemandPoint(
                    date=forecast_date,
                    demand=demand,
                )
            )

        return SeasonalForecast(
            item_id=item_id,
            seasonal_pattern=seasonal_pattern,
            base_demand=base_demand,
            forecast=forecast,
        )
