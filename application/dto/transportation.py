from dataclasses import dataclass
from typing import Optional


@dataclass
class LocationDTO:
    latitude: float
    longitude: float
    address: Optional[str] = None


@dataclass
class ShipmentDTO:
    id: str
    order_id: str
    tracking_number: str
    status: str
    estimated_arrival: str


@dataclass
class TrackShipmentResponse:
    shipment_id: str
    status: str
    current_location: Optional[LocationDTO]
    estimated_arrival: str
