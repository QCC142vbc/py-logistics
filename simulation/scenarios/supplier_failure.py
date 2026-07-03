from datetime import datetime, timedelta
from typing import List

from src.simulation.models.events import DisruptionEvent, SimulationEvent


def create_supplier_failure_scenario(
    supplier_id: str,
    recovery_time_days: int,
) -> List[SimulationEvent]:
    """Create a supplier failure scenario."""
    events: List[SimulationEvent] = []
    
    disruption = DisruptionEvent.create(
        disruption_type=DisruptionType.SUPPLIER_FAILURE,
        affected_entities=[supplier_id],
        duration_hours=recovery_time_days * 24,
        severity="high",
        timestamp=datetime.utcnow(),
    )
    events.append(disruption)

    return events
