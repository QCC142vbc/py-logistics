from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.domain.common.models import Location
from src.domain.transportation.models import TransportMode


@dataclass
class Delivery:
    location: Location
    demand: int
    time_window_start: str
    time_window_end: str
    service_time_minutes: int


@dataclass
class RoutingConstraints:
    max_distance_km: float = None
    max_duration_hours: float = None
    vehicle_capacity_kg: float = None
    time_windows: bool = True


@dataclass
class OptimizedRoute:
    route: List[Location]
    total_distance: float
    total_time: float
    cost: Decimal
    stops: List[dict]


@dataclass
class MultiDepotSolution:
    routes: List[OptimizedRoute]
    total_cost: Decimal
    total_distance: float


class RoutingOptimizer:
    """Optimizes vehicle routing problems."""

    def optimize_vehicle_route(
        self,
        depot: Location,
        deliveries: List[Delivery],
        constraints: RoutingConstraints,
    ) -> OptimizedRoute:
        """Optimize a single vehicle route using nearest neighbor heuristic."""
        if not deliveries:
            return OptimizedRoute(
                route=[depot],
                total_distance=0.0,
                total_time=0.0,
                cost=Decimal("0.00"),
                stops=[],
            )

        # Simplified nearest neighbor algorithm
        unvisited = deliveries.copy()
        current_location = depot
        route = [depot]
        total_distance = 0.0
        total_time = 0.0
        stops = []

        while unvisited:
            # Find nearest unvisited delivery
            nearest = min(
                unvisited,
                key=lambda d: current_location.distance_to(d.location),
            )

            distance = current_location.distance_to(nearest.location)
            travel_time = distance / 60  # Assume 60 km/h

            total_distance += distance
            total_time += travel_time + (nearest.service_time_minutes / 60)

            route.append(nearest.location)
            stops.append(
                {
                    "location": nearest.location,
                    "demand": nearest.demand,
                    "arrival_time": f"{total_time:.1f}h",
                }
            )

            current_location = nearest.location
            unvisited.remove(nearest)

        # Return to depot
        return_distance = current_location.distance_to(depot)
        total_distance += return_distance
        total_time += return_distance / 60
        route.append(depot)

        cost = Decimal(str(total_distance * 0.5))  # $0.50 per km

        return OptimizedRoute(
            route=route,
            total_distance=total_distance,
            total_time=total_time,
            cost=cost,
            stops=stops,
        )

    def optimize_multi_depot(
        self,
        depots: List[Location],
        deliveries: List[Delivery],
    ) -> MultiDepotSolution:
        """Optimize routing for multiple depots."""
        # Simplified: assign deliveries to nearest depot, then optimize each
        depot_assignments = {depot: [] for depot in depots}

        for delivery in deliveries:
            nearest_depot = min(
                depots,
                key=lambda d: d.distance_to(delivery.location),
            )
            depot_assignments[nearest_depot].append(delivery)

        routes = []
        total_cost = Decimal("0.00")
        total_distance = 0.0

        for depot, assigned_deliveries in depot_assignments.items():
            if assigned_deliveries:
                route = self.optimize_vehicle_route(
                    depot,
                    assigned_deliveries,
                    RoutingConstraints(),
                )
                routes.append(route)
                total_cost += route.cost
                total_distance += route.total_distance

        return MultiDepotSolution(
            routes=routes,
            total_cost=total_cost,
            total_distance=total_distance,
        )
