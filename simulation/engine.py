from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from src.simulation.models import SimulationEvent, SupplyChainNetwork


@dataclass
class SimulationMetrics:
    total_orders_processed: int
    fulfilled_orders: int
    stockout_events: int
    total_cost: Decimal
    average_fulfillment_time: float


@dataclass
class SimulatedEvent:
    timestamp: datetime
    event_type: str
    description: str
    impact: str


@dataclass
class Recommendation:
    action: str
    expected_benefit: str
    priority: str


@dataclass
class SimulationResult:
    metrics: SimulationMetrics
    events: List[SimulatedEvent]
    recommendations: List[Recommendation]


@dataclass
class DemandProfile:
    item_id: str
    base_demand: int
    variability: float  # coefficient of variation


@dataclass
class ScenarioResult:
    scenario_name: str
    fulfilled_orders: int
    stockout_percentage: float
    total_cost: Decimal
    recommendation: str


class SimulationEngine:
    """Simulates supply chain scenarios for what-if analysis."""

    def simulate_supply_chain(
        self,
        events: List[SimulationEvent],
        duration_days: int,
    ) -> SimulationResult:
        """Simulate supply chain operations over a period."""
        simulated_events: List[SimulatedEvent] = []
        
        # Process events in chronological order
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        
        for event in sorted_events:
            simulated_events.append(
                SimulatedEvent(
                    timestamp=event.timestamp,
                    event_type=event.event_type,
                    description=f"Processed {event.event_type}",
                    impact="normal",
                )
            )

        # Calculate metrics (simplified)
        metrics = SimulationMetrics(
            total_orders_processed=len([e for e in events if e.event_type == "demand"]),
            fulfilled_orders=int(len([e for e in events if e.event_type == "demand"]) * 0.95),
            stockout_events=5,
            total_cost=Decimal("50000.00"),
            average_fulfillment_time=3.5,
        )

        recommendations = [
            Recommendation(
                action="Increase safety stock for high-demand items",
                expected_benefit="Reduce stockouts by 30%",
                priority="high",
            ),
            Recommendation(
                action="Diversify supplier base",
                expected_benefit="Reduce supply disruption risk",
                priority="medium",
            ),
        ]

        return SimulationResult(
            metrics=metrics,
            events=simulated_events,
            recommendations=recommendations,
        )

    def simulate_demand_scenario(
        self,
        demand_profile: DemandProfile,
        inventory_levels: dict[str, int],
    ) -> ScenarioResult:
        """Simulate a demand scenario."""
        # Simplified simulation
        total_demand = demand_profile.base_demand * 30  # 30 days
        available_inventory = sum(inventory_levels.values())
        
        fulfilled = min(total_demand, available_inventory)
        stockout_pct = (total_demand - fulfilled) / total_demand * 100 if total_demand > 0 else 0

        return ScenarioResult(
            scenario_name="Demand Surge",
            fulfilled_orders=fulfilled,
            stockout_percentage=stockout_pct,
            total_cost=Decimal("25000.00"),
            recommendation="Increase reorder points by 20%" if stockout_pct > 10 else "Current levels adequate",
        )

    def simulate_disruption_scenario(
        self,
        disruption,
        network: SupplyChainNetwork,
    ) -> ScenarioResult:
        """Simulate a disruption scenario."""
        # Simplified disruption simulation
        return ScenarioResult(
            scenario_name=f"{disruption.disruption_type.value} Disruption",
            fulfilled_orders=int(100 * 0.7),  # 70% fulfillment during disruption
            stockout_percentage=30.0,
            total_cost=Decimal("75000.00"),
            recommendation="Activate backup suppliers and reroute shipments",
        )
