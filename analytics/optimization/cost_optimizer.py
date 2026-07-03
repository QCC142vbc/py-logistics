from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class CostRecommendation:
    description: str
    estimated_savings: Decimal
    implementation_cost: Decimal
    priority: str


@dataclass
class CostOptimizationResult:
    total_cost: Decimal
    savings: Decimal
    recommendations: List[CostRecommendation]


class CostOptimizer:
    """Optimizes costs across the supply chain."""

    def minimize_transportation_cost(
        self,
        shipments: List[dict],
        carriers: List[dict],
    ) -> CostOptimizationResult:
        """Minimize transportation costs by selecting optimal carriers."""
        # Simplified: select lowest cost carrier for each shipment
        recommendations = []
        total_savings = Decimal("0.00")

        for shipment in shipments:
            current_cost = shipment.get("current_cost", Decimal("0.00"))
            best_carrier = min(carriers, key=lambda c: c.get("rate", float("inf")))
            optimized_cost = Decimal(str(best_carrier["rate"] * shipment.get("distance", 1)))

            if optimized_cost < current_cost:
                savings = current_cost - optimized_cost
                total_savings += savings
                recommendations.append(
                    CostRecommendation(
                        description=f"Switch shipment {shipment['id']} to {best_carrier['name']}",
                        estimated_savings=savings,
                        implementation_cost=Decimal("0.00"),
                        priority="high" if savings > 100 else "medium",
                    )
                )

        return CostOptimizationResult(
            total_cost=Decimal("0.00"),
            savings=total_savings,
            recommendations=recommendations,
        )

    def optimize_warehouse_allocation(
        self,
        orders: List[dict],
        warehouses: List[dict],
    ) -> CostOptimizationResult:
        """Optimize warehouse allocation to minimize transportation costs."""
        # Simplified: assign orders to nearest warehouse
        recommendations = []
        total_savings = Decimal("0.00")

        for order in orders:
            order_location = order.get("location", {"lat": 0, "lon": 0})
            nearest_warehouse = min(
                warehouses,
                key=lambda w: self._calculate_distance(order_location, w["location"]),
            )

            current_warehouse = order.get("assigned_warehouse")
            if current_warehouse != nearest_warehouse["id"]:
                # Estimate savings from reduced distance
                savings = Decimal("50.00")  # Simplified
                total_savings += savings
                recommendations.append(
                    CostRecommendation(
                        description=f"Reassign order {order['id']} to warehouse {nearest_warehouse['id']}",
                        estimated_savings=savings,
                        implementation_cost=Decimal("10.00"),
                        priority="medium",
                    )
                )

        return CostOptimizationResult(
            total_cost=Decimal("0.00"),
            savings=total_savings,
            recommendations=recommendations,
        )

    def _calculate_distance(self, loc1: dict, loc2: dict) -> float:
        """Calculate distance between two locations."""
        lat_diff = loc1["lat"] - loc2["lat"]
        lon_diff = loc1["lon"] - loc2["lon"]
        return (lat_diff**2 + lon_diff**2) ** 0.5
