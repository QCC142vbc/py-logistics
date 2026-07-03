from dataclasses import dataclass
from decimal import Decimal
from typing import List

import httpx


@dataclass
class ShippingRate:
    carrier: str
    service_type: str
    cost: Decimal
    estimated_days: int


@dataclass
class ShipmentRequest:
    origin_address: str
    destination_address: str
    weight_kg: float
    dimensions: dict


@dataclass
class ShipmentConfirmation:
    tracking_number: str
    carrier: str
    estimated_delivery: str


@dataclass
class TrackingInfo:
    tracking_number: str
    status: str
    current_location: str
    estimated_delivery: str
    events: List[dict]


class CarrierAPIClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def get_rates(
        self,
        origin: str,
        destination: str,
        weight: float,
    ) -> List[ShippingRate]:
        """Get shipping rates from carriers."""
        response = await self._client.post(
            f"{self._base_url}/rates",
            json={
                "origin": origin,
                "destination": destination,
                "weight": weight,
            },
        )
        response.raise_for_status()
        data = response.json()
        
        return [
            ShippingRate(
                carrier=rate["carrier"],
                service_type=rate["service_type"],
                cost=Decimal(str(rate["cost"])),
                estimated_days=rate["estimated_days"],
            )
            for rate in data["rates"]
        ]

    async def create_shipment(self, request: ShipmentRequest) -> ShipmentConfirmation:
        """Create a shipment with the carrier."""
        response = await self._client.post(
            f"{self._base_url}/shipments",
            json={
                "origin": request.origin_address,
                "destination": request.destination_address,
                "weight": request.weight_kg,
                "dimensions": request.dimensions,
            },
        )
        response.raise_for_status()
        data = response.json()
        
        return ShipmentConfirmation(
            tracking_number=data["tracking_number"],
            carrier=data["carrier"],
            estimated_delivery=data["estimated_delivery"],
        )

    async def track_shipment(self, tracking_number: str) -> TrackingInfo:
        """Track a shipment."""
        response = await self._client.get(
            f"{self._base_url}/track/{tracking_number}"
        )
        response.raise_for_status()
        data = response.json()
        
        return TrackingInfo(
            tracking_number=data["tracking_number"],
            status=data["status"],
            current_location=data["current_location"],
            estimated_delivery=data["estimated_delivery"],
            events=data.get("events", []),
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
