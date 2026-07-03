from abc import ABC, abstractmethod
from typing import Awaitable

from src.domain.events.models import DomainEvent


class EventHandler(ABC):
    """Base class for event handlers."""

    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event."""
        pass

    @property
    @abstractmethod
    def event_type(self) -> str:
        """Return the event type this handler handles."""
        pass


class OrderCreatedHandler(EventHandler):
    """Handler for OrderCreatedEvent."""

    @property
    def event_type(self) -> str:
        return "OrderCreated"

    async def handle(self, event: DomainEvent) -> None:
        """Handle order created event."""
        # Send confirmation email, update analytics, etc.
        pass


class InventoryLowHandler(EventHandler):
    """Handler for InventoryLowEvent."""

    @property
    def event_type(self) -> str:
        return "InventoryLow"

    async def handle(self, event: DomainEvent) -> None:
        """Handle inventory low event."""
        # Create purchase order, send alert, etc.
        pass


class ShipmentDeliveredHandler(EventHandler):
    """Handler for ShipmentDeliveredEvent."""

    @property
    def event_type(self) -> str:
        return "ShipmentDelivered"

    async def handle(self, event: DomainEvent) -> None:
        """Handle shipment delivered event."""
        # Update order status, send notification, etc.
        pass
