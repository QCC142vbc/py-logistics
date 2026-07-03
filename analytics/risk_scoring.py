from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from src.domain.inventory.models import Item
from src.domain.supplier.models import Supplier


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskFactor:
    category: str
    description: str
    impact: float  # 0-100


@dataclass
class RiskScore:
    score: float
    level: RiskLevel
    factors: List[RiskFactor]


@dataclass
class SupplierHistory:
    delivery_records: List[dict]
    quality_records: List[dict]
    pricing_history: List[Decimal]


@dataclass
class DemandHistory:
    item_id: str
    daily_demand: List[int]
    lead_times: List[int]


@dataclass
class SupplyChainNetwork:
    nodes: List[dict]
    edges: List[dict]


@dataclass
class SupplyChainRiskReport:
    overall_risk: RiskScore
    supplier_risks: dict[str, RiskScore]
    inventory_risks: dict[str, RiskScore]
    transportation_risks: dict[str, RiskScore]
    recommendations: List[str]


class RiskScoringEngine:
    """Calculates various risk scores for the supply chain."""

    def calculate_supplier_risk(
        self,
        supplier: Supplier,
        historical_data: SupplierHistory,
    ) -> RiskScore:
        """Calculate risk score for a supplier."""
        factors: List[RiskFactor] = []

        # Delivery reliability risk
        on_time_rate = self._calculate_on_time_rate(historical_data.delivery_records)
        if on_time_rate < 0.8:
            factors.append(
                RiskFactor(
                    category="delivery",
                    description=f"Low on-time delivery rate: {on_time_rate:.1%}",
                    impact=(0.8 - on_time_rate) * 100,
                )
            )

        # Quality risk
        quality_rate = self._calculate_quality_rate(historical_data.quality_records)
        if quality_rate < 0.9:
            factors.append(
                RiskFactor(
                    category="quality",
                    description=f"Quality acceptance rate: {quality_rate:.1%}",
                    impact=(0.9 - quality_rate) * 100,
                )
            )

        # Financial risk (simplified)
        factors.append(
            RiskFactor(
                category="financial",
                description="Financial stability assessment",
                impact=10.0,
            )
        )

        # Calculate overall score
        total_impact = sum(f.impact for f in factors)
        base_score = 100 - total_impact
        score = max(0, min(100, base_score))

        # Determine risk level
        if score >= 80:
            level = RiskLevel.LOW
        elif score >= 60:
            level = RiskLevel.MEDIUM
        elif score >= 40:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        return RiskScore(score=score, level=level, factors=factors)

    def calculate_inventory_risk(
        self,
        item: Item,
        demand_history: DemandHistory,
    ) -> RiskScore:
        """Calculate risk score for inventory items."""
        factors: List[RiskFactor] = []

        # Stockout risk
        if item.quantity <= item.reorder_point:
            factors.append(
                RiskFactor(
                    category="stockout",
                    description=f"Stock below reorder point: {item.quantity} <= {item.reorder_point}",
                    impact=50.0,
                )
            )

        # Demand volatility risk
        volatility = self._calculate_demand_volatility(demand_history.daily_demand)
        if volatility > 0.3:
            factors.append(
                RiskFactor(
                    category="volatility",
                    description=f"High demand volatility: {volatility:.1%}",
                    impact=volatility * 100,
                )
            )

        # Obsolescence risk (simplified)
        factors.append(
            RiskFactor(
                category="obsolescence",
                description="Obsolescence risk assessment",
                impact=5.0,
            )
        )

        total_impact = sum(f.impact for f in factors)
        base_score = 100 - total_impact
        score = max(0, min(100, base_score))

        if score >= 80:
            level = RiskLevel.LOW
        elif score >= 60:
            level = RiskLevel.MEDIUM
        elif score >= 40:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        return RiskScore(score=score, level=level, factors=factors)

    def calculate_supply_chain_risk(
        self,
        network: SupplyChainNetwork,
    ) -> SupplyChainRiskReport:
        """Calculate overall supply chain risk."""
        # Simplified implementation
        overall_score = RiskScore(
            score=65.0,
            level=RiskLevel.MEDIUM,
            factors=[
                RiskFactor(category="network", description="Network complexity", impact=20.0),
                RiskFactor(category="geographic", description="Geographic concentration", impact=15.0),
            ],
        )

        return SupplyChainRiskReport(
            overall_risk=overall_score,
            supplier_risks={},
            inventory_risks={},
            transportation_risks={},
            recommendations=[
                "Diversify supplier base",
                "Increase safety stock for critical items",
                "Implement real-time tracking",
            ],
        )

    def _calculate_on_time_rate(self, delivery_records: List[dict]) -> float:
        """Calculate on-time delivery rate."""
        if not delivery_records:
            return 0.9  # Default assumption
        on_time = sum(1 for r in delivery_records if r.get("on_time", False))
        return on_time / len(delivery_records)

    def _calculate_quality_rate(self, quality_records: List[dict]) -> float:
        """Calculate quality acceptance rate."""
        if not quality_records:
            return 0.95  # Default assumption
        total_inspected = sum(r.get("total", 0) for r in quality_records)
        total_passed = sum(r.get("passed", 0) for r in quality_records)
        return total_passed / total_inspected if total_inspected > 0 else 0.95

    def _calculate_demand_volatility(self, daily_demand: List[int]) -> float:
        """Calculate demand volatility (coefficient of variation)."""
        if not daily_demand or len(daily_demand) < 2:
            return 0.0

        import statistics

        mean = statistics.mean(daily_demand)
        if mean == 0:
            return 0.0

        stdev = statistics.stdev(daily_demand)
        return stdev / mean
