from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: str
    event_type: str
    aggregate_id: str
    data: Dict[str, Any]
    occurred_at: datetime
    version: int = 1

    @classmethod
    def create(
        cls,
        event_type: str,
        aggregate_id: str,
        data: Dict[str, Any],
    ) -> "DomainEvent":
        return cls(
            event_id=str(uuid4()),
            event_type=event_type,
            aggregate_id=aggregate_id,
            data=data,
            occurred_at=datetime.utcnow(),
        )


@dataclass
class OrderCreatedEvent(DomainEvent):
    """Event raised when an order is created."""
    order_id: str
    customer_id: str
    total_amount: float

    @classmethod
    def create(
        cls,
        order_id: str,
        customer_id: str,
        total_amount: float,
    ) -> "OrderCreatedEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="OrderCreated",
            aggregate_id=order_id,
            data={
                "order_id": order_id,
                "customer_id": customer_id,
                "total_amount": total_amount,
            },
            occurred_at=datetime.utcnow(),
            order_id=order_id,
            customer_id=customer_id,
            total_amount=total_amount,
        )


@dataclass
class InventoryLowEvent(DomainEvent):
    """Event raised when inventory falls below reorder point."""
    item_id: str
    sku: str
    current_quantity: int
    reorder_point: int

    @classmethod
    def create(
        cls,
        item_id: str,
        sku: str,
        current_quantity: int,
        reorder_point: int,
    ) -> "InventoryLowEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="InventoryLow",
            aggregate_id=item_id,
            data={
                "item_id": item_id,
                "sku": sku,
                "current_quantity": current_quantity,
                "reorder_point": reorder_point,
            },
            occurred_at=datetime.utcnow(),
            item_id=item_id,
            sku=sku,
            current_quantity=current_quantity,
            reorder_point=reorder_point,
        )


@dataclass
class ShipmentDeliveredEvent(DomainEvent):
    """Event raised when a shipment is delivered."""
    shipment_id: str
    order_id: str
    tracking_number: str
    delivery_date: datetime

    @classmethod
    def create(
        cls,
        shipment_id: str,
        order_id: str,
        tracking_number: str,
        delivery_date: datetime,
    ) -> "ShipmentDeliveredEvent":
        return cls(
            event_id=str(uuid4()),
            event_type="ShipmentDelivered",
            aggregate_id=shipment_id,
            data={
                "shipment_id": shipment_id,
                "order_id": order_id,
                "tracking_number": tracking_number,
                "delivery_date": delivery_date.isoformat(),
            },
            occurred_at=datetime.utcnow(),
            shipment_id=shipment_id,
            order_id=order_id,
            tracking_number=tracking_number,
            delivery_date=delivery_date,
        )
