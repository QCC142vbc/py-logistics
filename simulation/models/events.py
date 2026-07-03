from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class DisruptionType(Enum):
    PORT_CLOSURE = "port_closure"
    SUPPLIER_FAILURE = "supplier_failure"
    TRANSPORTATION_STRIKE = "transportation_strike"
    NATURAL_DISASTER = "natural_disaster"


@dataclass
class SimulationEvent:
    event_id: str
    event_type: str
    timestamp: datetime
    parameters: Dict[str, any]

    @classmethod
    def create(
        cls,
        event_type: str,
        timestamp: datetime,
        parameters: Dict[str, any],
    ) -> "SimulationEvent":
        return cls(
            event_id=str(uuid4()),
            event_type=event_type,
            timestamp=timestamp,
            parameters=parameters,
        )


@dataclass
class DemandEvent(SimulationEvent):
    item_id: str
    quantity: int

    @classmethod
    def create(
        cls,
        item_id: str,
        quantity: int,
        timestamp: Optional[datetime] = None,
    ) -> "DemandEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="demand",
            timestamp=timestamp or datetime.utcnow(),
            parameters={"item_id": item_id, "quantity": quantity},
            item_id=item_id,
            quantity=quantity,
        )


@dataclass
class SupplyEvent(SimulationEvent):
    item_id: str
    quantity: int
    supplier_id: str

    @classmethod
    def create(
        cls,
        item_id: str,
        quantity: int,
        supplier_id: str,
        timestamp: Optional[datetime] = None,
    ) -> "SupplyEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="supply",
            timestamp=timestamp or datetime.utcnow(),
            parameters={"item_id": item_id, "quantity": quantity, "supplier_id": supplier_id},
            item_id=item_id,
            quantity=quantity,
            supplier_id=supplier_id,
        )


@dataclass
class DisruptionEvent(SimulationEvent):
    disruption_type: DisruptionType
    affected_entities: List[str]
    duration_hours: int
    severity: str = "medium"

    @classmethod
    def create(
        cls,
        disruption_type: DisruptionType,
        affected_entities: List[str],
        duration_hours: int,
        severity: str = "medium",
        timestamp: Optional[datetime] = None,
    ) -> "DisruptionEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="disruption",
            timestamp=timestamp or datetime.utcnow(),
            parameters={
                "disruption_type": disruption_type,
                "affected_entities": affected_entities,
                "duration_hours": duration_hours,
                "severity": severity,
            },
            disruption_type=disruption_type,
            affected_entities=affected_entities,
            duration_hours=duration_hours,
            severity=severity,
        )
