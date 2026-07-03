from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Optional

from src.application.dto.common import LocationDTO
from src.domain.common.models import Location
from src.domain.transportation.models import Route, TransportMode
from src.domain.transportation.services import RouteConstraints, TransportationService


@dataclass
class RouteConstraintsDTO:
    max_distance_km: float = None
    max_duration_hours: float = None
    max_cost: Decimal = None
    preferred_modes: List[str] = None
    avoid_carriers: List[str] = None


@dataclass
class RouteStepDTO:
    location: LocationDTO
    transport_mode: str
    distance_km: float
    duration_hours: float
    cost: str


@dataclass
class PlanRouteRequest:
    origin: LocationDTO
    destination: LocationDTO
    constraints: RouteConstraintsDTO


@dataclass
class PlanRouteResponse:
    route_id: str
    distance_km: float
    estimated_duration_hours: float
    cost: str
    steps: List[RouteStepDTO]


class PlanRouteUseCase:
    def __init__(self, transportation_service: TransportationService) -> None:
        self._transportation_service = transportation_service

    async def execute(self, request: PlanRouteRequest) -> PlanRouteResponse:
        origin = Location(
            latitude=request.origin.latitude,
            longitude=request.origin.longitude,
            address=request.origin.address,
        )

        destination = Location(
            latitude=request.destination.latitude,
            longitude=request.destination.longitude,
            address=request.destination.address,
        )

        constraints = RouteConstraints(
            max_distance_km=request.constraints.max_distance_km,
            max_duration_hours=request.constraints.max_duration_hours,
            max_cost=request.constraints.max_cost,
            preferred_modes=[
                TransportMode(m) for m in (request.constraints.preferred_modes or [])
            ],
            avoid_carriers=request.constraints.avoid_carriers,
        )

        route = await self._transportation_service.plan_route(origin, destination, constraints)

        steps = [
            RouteStepDTO(
                location=LocationDTO(
                    latitude=route.origin.latitude,
                    longitude=route.origin.longitude,
                    address=route.origin.address,
                ),
                transport_mode=route.transport_mode.value,
                distance_km=route.distance_km,
                duration_hours=route.estimated_duration_hours,
                cost=str(route.cost),
            )
        ]

        return PlanRouteResponse(
            route_id=route.id,
            distance_km=route.distance_km,
            estimated_duration_hours=route.estimated_duration_hours,
            cost=str(route.cost),
            steps=steps,
        )
