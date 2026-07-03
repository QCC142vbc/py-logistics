from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class EconomicOrderQuantity:
    quantity: int
    order_frequency: float  # orders per year
    total_cost: Decimal


@dataclass
class SafetyStockLevel:
    quantity: int
    service_level: float
    lead_time_std_dev: float


@dataclass
class ReorderPointRecommendation:
    item_id: str
    current_reorder_point: int
    recommended_reorder_point: int
    estimated_savings: Decimal


class InventoryOptimizer:
    """Optimizes inventory levels and reorder points."""

    def calculate_eoq(
        self,
        demand_rate: float,  # annual demand
        ordering_cost: Decimal,
        holding_cost: Decimal,  # annual holding cost per unit
    ) -> EconomicOrderQuantity:
        """Calculate Economic Order Quantity using EOQ formula."""
        from math import sqrt

        # EOQ = sqrt(2 * D * S / H)
        eoq = sqrt(2 * demand_rate * float(ordering_cost) / float(holding_cost))
        quantity = int(round(eoq))

        order_frequency = demand_rate / quantity if quantity > 0 else 0

        # Total cost = ordering cost + holding cost
        total_ordering_cost = (demand_rate / quantity) * ordering_cost if quantity > 0 else Decimal("0")
        total_holding_cost = (quantity / 2) * holding_cost
        total_cost = total_ordering_cost + total_holding_cost

        return EconomicOrderQuantity(
            quantity=quantity,
            order_frequency=order_frequency,
            total_cost=total_cost,
        )

    def calculate_safety_stock(
        self,
        demand_std_dev: float,
        lead_time_std_dev: float,
        service_level: float,
        average_demand: float,
        average_lead_time: float,
    ) -> SafetyStockLevel:
        """Calculate safety stock using service level approach."""
        from math import sqrt
        from scipy.stats import norm

        # Z-score for service level
        z_score = norm.ppf(service_level)

        # Safety stock = Z * sqrt((LT * σd²) + (D² * σLT²))
        safety_stock = z_score * sqrt(
            (average_lead_time * demand_std_dev**2)
            + (average_demand**2 * lead_time_std_dev**2)
        )

        return SafetyStockLevel(
            quantity=int(round(safety_stock)),
            service_level=service_level,
            lead_time_std_dev=lead_time_std_dev,
        )

    def optimize_reorder_points(
        self,
        items: List[dict],
    ) -> List[ReorderPointRecommendation]:
        """Optimize reorder points for multiple items."""
        recommendations = []

        for item in items:
            # Simplified calculation
            current_rp = item.get("reorder_point", 0)
            demand_rate = item.get("annual_demand", 100)
            lead_time_days = item.get("lead_time_days", 7)

            # Recommended RP = (daily demand * lead time) + safety stock
            daily_demand = demand_rate / 365
            safety_stock = daily_demand * 3  # 3 days safety stock
            recommended_rp = int(daily_demand * lead_time_days + safety_stock)

            # Estimate savings (reduced stockouts)
            estimated_savings = Decimal(str(abs(recommended_rp - current_rp) * 0.5))

            recommendations.append(
                ReorderPointRecommendation(
                    item_id=item["id"],
                    current_reorder_point=current_rp,
                    recommended_reorder_point=recommended_rp,
                    estimated_savings=estimated_savings,
                )
            )

        return recommendations
