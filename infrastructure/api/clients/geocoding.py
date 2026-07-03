from dataclasses import dataclass

import httpx

from src.domain.common.models import Location
from src.domain.supplier.models import Address


@dataclass
class GeocodingResponse:
    latitude: float
    longitude: float
    formatted_address: str


class GeocodingAPIClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._base_url = "https://api.geocoding-service.com"
        self._client = httpx.AsyncClient(
            headers={"X-API-Key": api_key}
        )

    async def geocode(self, address: str) -> Location:
        """Convert an address to coordinates."""
        response = await self._client.get(
            f"{self._base_url}/geocode",
            params={"address": address},
        )
        response.raise_for_status()
        data = response.json()
        
        return Location(
            latitude=data["latitude"],
            longitude=data["longitude"],
            address=data["formatted_address"],
        )

    async def reverse_geocode(
        self,
        latitude: float,
        longitude: float,
    ) -> Address:
        """Convert coordinates to an address."""
        response = await self._client.get(
            f"{self._base_url}/reverse",
            params={"lat": latitude, "lon": longitude},
        )
        response.raise_for_status()
        data = response.json()
        
        return Address(
            street=data["street"],
            city=data["city"],
            state=data["state"],
            postal_code=data["postal_code"],
            country=data["country"],
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
