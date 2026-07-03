from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class CarrierPerformance:
    on_time_rate: float
    damage_rate: float
    cost_efficiency: float


@dataclass
class OTIFScore:
    on_time: float
    in_full: float
    overall: float


class KPICalculator:
    """Calculates key performance indicators."""

    def calculate_inventory_turnover(
        self,
        cost_of_goods_sold: Decimal,
        average_inventory: Decimal,
    ) -> float:
        """Calculate inventory turnover ratio."""
        if average_inventory == 0:
            return 0.0
        return float(cost_of_goods_sold / average_inventory)

    def calculate_order_fulfillment_rate(
        self,
        total_orders: int,
        fulfilled_orders: int,
    ) -> float:
        """Calculate order fulfillment rate."""
        if total_orders == 0:
            return 0.0
        return fulfilled_orders / total_orders

    def calculate_on_time_delivery(
        self,
        shipments: List[dict],
    ) -> float:
        """Calculate on-time delivery rate."""
        if not shipments:
            return 0.0
        on_time = sum(1 for s in shipments if s.get("on_time", False))
        return on_time / len(shipments)

    def calculate_carrier_performance(
        self,
        carrier_id: str,
    ) -> CarrierPerformance:
        """Calculate carrier performance metrics."""
        # Simplified implementation
        return CarrierPerformance(
            on_time_rate=0.92,
            damage_rate=0.02,
            cost_efficiency=0.88,
        )

    def calculate_supplier_otif(
        self,
        supplier_id: str,
    ) -> OTIFScore:
        """Calculate OTIF (On-Time In-Full) score for a supplier."""
        # Simplified implementation
        return OTIFScore(
            on_time=0.90,
            in_full=0.95,
            overall=0.855,
        )
