from datetime import datetime, timedelta
from typing import List

from src.simulation.models.events import DemandEvent, SimulationEvent


def create_demand_surge_scenario(
    surge_percentage: float,
    duration_days: int,
    base_demand: int = 10,
) -> List[SimulationEvent]:
    """Create a demand surge scenario."""
    events: List[SimulationEvent] = []
    base_date = datetime.utcnow()

    for day in range(duration_days):
        # Demand increases by surge_percentage
        demand = int(base_demand * (1 + surge_percentage))
        event = DemandEvent.create(
            item_id="ITEM-001",
            quantity=demand,
            timestamp=base_date + timedelta(days=day),
        )
        events.append(event)

    return events
