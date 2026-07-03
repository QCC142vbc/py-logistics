from datetime import datetime, timedelta
from typing import List

from src.simulation.models.events import DisruptionEvent, SimulationEvent


def create_port_disruption_scenario(
    port_id: str,
    duration_days: int,
) -> List[SimulationEvent]:
    """Create a port disruption scenario."""
    events: List[SimulationEvent] = []
    
    disruption = DisruptionEvent.create(
        disruption_type=DisruptionType.PORT_CLOSURE,
        affected_entities=[port_id],
        duration_hours=duration_days * 24,
        severity="critical",
        timestamp=datetime.utcnow(),
    )
    events.append(disruption)

    return events
