from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from src.domain.common.models import Location
from src.domain.transportation.models import Route, TransportMode
from src.domain.transportation.services import RouteConstraints


@dataclass
class TransportGraph:
    """Graph representation of transportation network."""
    nodes: List[Location]
    edges: List["TransportEdge"]


@dataclass
class TransportEdge:
    from_node: Location
    to_node: Location
    distance_km: float
    duration_hours: float
    cost: Decimal
    transport_mode: TransportMode
    carrier_id: Optional[str] = None


@dataclass
class RouteStep:
    location: Location
    transport_mode: TransportMode
    distance_km:(float)
    duration_hours: float
    cost: Decimal


class RoutingEngine:
    """Engine for calculating optimal routes."""

    def __init__(self) -> None:
        self._graph: Optional[TransportGraph] = None

    def find_shortest_path(
        self,
        origin: Location,
        destination: Location,
        constraints: RouteConstraints,
    ) -> Route:
        """
        Find the shortest path between two locations.
        Uses Dijkstra's algorithm for shortest path calculation.
        """
        # In a real implementation, this would query a graph database
        # For now, return a simplified route
        distance_km = self._calculate_distance(origin, destination)
        duration_hours = distance_km / 80  # Assume 80 km/h average
        cost = Decimal(distance_km) * Decimal("0.5")  # $0.50 per km

        return Route(
            origin=origin,
            destination=destination,
            distance_km=distance_km,
            estimated_duration_hours=duration_hours,
            cost=cost,
            transport_mode=TransportMode.TRUCK,
        )

    def find_cheapest_path(
        self,
        origin: Location,
        destination: Location,
        constraints: RouteConstraints,
    ) -> Route:
        """Find the cheapest path between two locations."""
        distance_km = self._calculate_distance(origin, destination)
        duration_hours = distance_km / 60  # Slower but cheaper
        cost = Decimal(distance_km) * Decimal("0.3")  # $0.30 per km

        return Route(
            origin=origin,
            destination=destination,
            distance_km=distance_km,
            estimated_duration_hours=duration_hours,
            cost=cost,
            transport_mode=TransportMode.RAIL,
        )

    def find_fastest_path(
        self,
        origin: Location,
        destination: Location,
        constraints: RouteConstraints,
    ) -> Route:
        """Find the fastest path between two locations."""
        distance_km = self._calculate_distance(origin, destination)
        duration_hours = distance_km / 800  # Assume 800 km/h for air
        cost = Decimal(distance_km) * Decimal("2.0")  # $2.00 per km

        return Route(
            origin=origin,
            destination=destination,
            distance_km=distance_km,
            estimated_duration_hours=duration_hours,
            cost=cost,
            transport_mode=TransportMode.AIR,
        )

    def optimize_multi_stop(
        self,
        locations: List[Location],
        constraints: RouteConstraints,
    ) -> List[Route]:
        """
        Optimize a route with multiple stops.
        Uses a simplified traveling salesman approach.
        """
        if len(locations) < 2:
            return []

        routes: List[Route] = []
        for i in range(len(locations) - 1):
            route = self.find_shortest_path(
                locations[i],
                locations[i + 1],
                constraints,
            )
            routes.append(route)

        return routes

    def _calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate distance between two locations using Haversine formula."""
        from math import asin, cos, radians, sin, sqrt

        R = 6371  # Earth's radius in km

        lat1 = radians(origin.latitude)
        lon1 = radians(origin.longitude)
        lat2 = radians(destination.latitude)
        lon2 = radians(destination.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        return R * c
