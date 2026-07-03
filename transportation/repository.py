from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.domain.transportation.models import Route, Shipment, Carrier, ShipmentStatus, TransportMode


@dataclass
class RouteFilter:
    origin: Optional[str] = None
    destination: Optional[str] = None
    transport_mode: Optional[TransportMode] = None
    active_only: bool = True
    carrier_id: Optional[str] = None


@dataclass
class ShipmentFilter:
    order_id: Optional[str] = None
    status: Optional[ShipmentStatus] = None
    carrier: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    tracking_number: Optional[str] = None


class TransportationRepository(ABC):
    @abstractmethod
    async def get_shipment(self, shipment_id: str) -> Optional[Shipment]:
        """Retrieve a shipment by ID."""
        pass

    @abstractmethod
    async def get_shipment_by_tracking(self, tracking_number: str) -> Optional[Shipment]:
        """Retrieve a shipment by tracking number."""
        pass

    @abstractmethod
    async def save_shipment(self, shipment: Shipment) -> None:
        """Save or update a shipment."""
        pass

    @abstractmethod
    async def delete_shipment(self, shipment_id: str) -> None:
        """Delete a shipment by ID."""
        pass

    @abstractmethod
    async def list_shipments(self, filter: ShipmentFilter) -> List[Shipment]:
        """List shipments based on filter criteria."""
        pass

    @abstractmethod
    async def get_route(self, route_id: str) -> Optional[Route]:
        """Retrieve a route by ID."""
        pass

    @abstractmethod
    async def save_route(self, route: Route) -> None:
        """Save or update a route."""
        pass

    @abstractmethod
    async def delete_route(self, route_id: str) -> None:
        """Delete a route by ID."""
        pass

    @abstractmethod
    async def list_routes(self, filter: RouteFilter) -> List[Route]:
        """List routes based on filter criteria."""
        pass

    @abstractmethod
    async def get_carrier(self, carrier_id: str) -> Optional[Carrier]:
        """Retrieve a carrier by ID."""
        pass

    @abstractmethod
    async def save_carrier(self, carrier: Carrier) -> None:
        """Save or update a carrier."""
        pass

    @abstractmethod
    async def delete_carrier(self, carrier_id: str) -> None:
        """Delete a carrier by ID."""
        pass

    @abstractmethod
    async def list_carriers(self, active_only: bool = True) -> List[Carrier]:
        """List all carriers."""
        pass

    @abstractmethod
    async def get_active_carriers(self) -> List[Carrier]:
        """Retrieve all active carriers."""
        pass

    @abstractmethod
    async def get_shipments_by_order(self, order_id: str) -> List[Shipment]:
        """Retrieve all shipments for an order."""
        pass

    @abstractmethod
    async def get_shipments_by_status(self, status: ShipmentStatus) -> List[Shipment]:
        """Retrieve all shipments with a specific status."""
        pass

    @abstractmethod
    async def get_delayed_shipments(self) -> List[Shipment]:
        """Retrieve all delayed shipments."""
        pass

    @abstractmethod
    async def get_routes_by_carrier(self, carrier_id: str) -> List[Route]:
        """Retrieve all routes for a carrier."""
        pass

    @abstractmethod
    async def search_carriers(self, query: str) -> List[Carrier]:
        """Search carriers by name or other fields."""
        pass
