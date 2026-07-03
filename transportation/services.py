from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from src.domain.common.models import Location
from src.domain.transportation.exceptions import (
    CarrierUnavailableError,
    RouteNotFoundError,
    ShipmentNotFoundError,
)
from src.domain.transportation.models import (
    Carrier,
    CarrierService,
    Route,
    Shipment,
    ShipmentItem,
    ShipmentStatus,
    TransportMode,
)
from src.domain.transportation.repository import (
    RouteFilter,
    ShipmentFilter,
    TransportationRepository,
)
from src.domain.transportation.routing import RoutingEngine


@dataclass
class RouteConstraints:
    max_distance_km: Optional[float] = None
    max_duration_hours: Optional[float] = None
    max_cost: Optional[Decimal] = None
    preferred_modes: Optional[List[TransportMode]] = None
    avoid_carriers: Optional[List[str]] = None


@dataclass
class ShipmentRequirements:
    weight_kg: float
    volume_m3: float
    priority: str = "standard"  # standard, expedited, economy
    special_handling: bool = False
    temperature_controlled: bool = False
    hazardous: bool = False


@dataclass
class ShippingRate:
    carrier_id: str
    carrier_name: str
    service_type: str
    cost: Decimal
    estimated_duration_hours: float
    estimated_arrival: datetime


class TransportationService:
    def __init__(
        self,
        repo: TransportationRepository,
        routing_engine: RoutingEngine,
    ) -> None:
        self._repo = repo
        self._routing_engine = routing_engine

    async def create_shipment(self, shipment: Shipment) -> Shipment:
        """Create a new shipment."""
        # Validate route exists
        route = await self._repo.get_route(shipment.route_id)
        if not route:
            raise RouteNotFoundError(f"Route {shipment.route_id} not found")

        # Validate carrier exists and is active
        carrier = await self._repo.get_carrier(shipment.carrier)
        if not carrier or not carrier.active:
            raise CarrierUnavailableError(f"Carrier {shipment.carrier} is unavailable")

        shipment.status = ShipmentStatus.PENDING
        await self._repo.save_shipment(shipment)
        return shipment

    async def get_shipment(self, shipment_id: str) -> Shipment:
        """Retrieve a shipment by ID."""
        shipment = await self._repo.get_shipment(shipment_id)
        if not shipment:
            raise ShipmentNotFoundError(f"Shipment with ID {shipment_id} not found")
        return shipment

    async def track_shipment(self, shipment_id: str) -> ShipmentStatus:
        """Track the current status of a shipment."""
        shipment = await self.get_shipment(shipment_id)
        return shipment.status

    async def track_by_tracking_number(self, tracking_number: str) -> Shipment:
        """Track a shipment by tracking number."""
        shipment = await self._repo.get_shipment_by_tracking(tracking_number)
        if not shipment:
            raise ShipmentNotFoundError(
                f"Shipment with tracking number {tracking_number} not found"
            )
        return shipment

    async def update_shipment_status(
        self,
        shipment_id: str,
        status: ShipmentStatus,
        current_location: Optional[Location] = None,
    ) -> Shipment:
        """Update the status of a shipment."""
        shipment = await self.get_shipment(shipment_id)
        shipment.status = status
        shipment.current_location = current_location

        if status == ShipmentStatus.PICKED_UP:
            shipment.pickup_date = datetime.utcnow()
        elif status == ShipmentStatus.DELIVERED:
            shipment.delivery_date = datetime.utcnow()
            shipment.actual_arrival = datetime.utcnow()

        await self._repo.save_shipment(shipment)
        return shipment

    async def plan_route(
        self,
        origin: Location,
        destination: Location,
        constraints: RouteConstraints,
    ) -> Route:
        """Plan a route between two locations."""
        route = self._routing_engine.find_shortest_path(
            origin,
            destination,
            constraints,
        )
        await self._repo.save_route(route)
        return route

    async def select_carrier(
        self,
        route: Route,
        requirements: ShipmentRequirements,
    ) -> Carrier:
        """Select the best carrier for a route based on requirements."""
        carriers = await self._repo.get_active_carriers()
        
        # Filter carriers that can handle the requirements
        suitable_carriers = []
        for carrier in carriers:
            for service in carrier.services:
                if (
                    service.max_weight_kg >= requirements.weight_kg
                    and (requirements.volume_m3 or 0) <= (service.max_volume_m3 or float("inf"))
                ):
                    suitable_carriers.append(carrier)
                    break

        if not suitable_carriers:
            raise CarrierUnavailableError("No carrier available for these requirements")

        # Select best carrier by rating
        best_carrier = max(suitable_carriers, key=lambda c: c.rating)
        return best_carrier

    async def calculate_shipping_cost(
        self,
        route: Route,
        weight_kg: float,
        volume_m3: float,
    ) -> Decimal:
        """Calculate shipping cost for a route."""
        carriers = await self._repo.get_active_carriers()
        
        rates: List[ShippingRate] = []
        for carrier in carriers:
            for service in carrier.services:
                if service.max_weight_kg >= weight_kg:
                    cost = service.base_rate + (service.rate_per_km * Decimal(route.distance_km))
                    rates.append(
                        ShippingRate(
                            carrier_id=carrier.id,
                            carrier_name=carrier.name,
                            service_type=service.service_type,
                            cost=cost,
                            estimated_duration_hours=route.estimated_duration_hours,
                            estimated_arrival=datetime.utcnow()
                            + datetime.timedelta(hours=route.estimated_duration_hours),
                        )
                    )

        if not rates:
            raise CarrierUnavailableError("No carrier available for these requirements")

        # Return the lowest cost
        return min(rates, key=lambda r: r.cost).cost

    async def get_shipping_rates(
        self,
        origin: Location,
        destination: Location,
        requirements: ShipmentRequirements,
    ) -> List[ShippingRate]:
        """Get shipping rates from multiple carriers."""
        carriers = await self._repo.get_active_carriers()
        
        rates: List[ShippingRate] = []
        for carrier in carriers:
            for service in carrier.services:
                if service.max_weight_kg >= requirements.weight_kg:
                    # Calculate distance (simplified)
                    distance_km = self._calculate_distance(origin, destination)
                    cost = service.base_rate + (service.rate_per_km * Decimal(distance_km))
                    rates.append(
                        ShippingRate(
                            carrier_id=carrier.id,
                            carrier_name=carrier.name,
                            service_type=service.service_type,
                            cost=cost,
                            estimated_duration_hours=distance_km / 80,  # Simplified
                            estimated_arrival=datetime.utcnow()
                            + datetime.timedelta(hours=distance_km / 80),
                        )
                    )

        return sorted(rates, key=lambda r: r.cost)

    async def cancel_shipment(self, shipment_id: str, reason: str) -> bool:
        """Cancel a shipment."""
        if not shipment.can_be_cancelled:
            raise ShipmentNotFoundError(
                f"Shipment {shipment_id} cannot be cancelled in its current state"
            )

        shipment = await self.get_shipment(shipment_id)
        shipment.status = ShipmentStatus.CANCELLED
        shipment.notes = f"{shipment.notes or ''}\nCancelled: {reason}"
        await self._repo.save_shipment(shipment)
        return True

    async def list_shipments(
        self,
        filter: Optional[ShipmentFilter] = None,
    ) -> List[Shipment]:
        """List shipments based on filter criteria."""
        if filter is None:
            filter = ShipmentFilter()
        return await self._repo.list_shipments(filter)

    async def list_routes(
        self,
        filter: Optional[RouteFilter] = None,
    ) -> List[Route]:
        """List routes based on filter criteria."""
        if filter is None:
            filter = RouteFilter()
        return await self._repo.list_routes(filter)

    async def list_carriers(self, active_only: bool = True) -> List[Carrier]:
        """List all carriers."""
        return await self._repo.list_carriers(active_only)

    def _calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate distance between two locations (simplified)."""
        # In a real implementation, this would use a geospatial library
        lat_diff = abs(origin.latitude - destination.latitude)
        lon_diff = abs(origin.longitude - destination.longitude)
        return ((lat_diff ** 2) + (lon_diff ** 2)) ** 0.5 * 111  # Rough km conversion
