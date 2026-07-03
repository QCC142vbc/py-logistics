from dataclasses import dataclass
from datetime import time
from typing import List

from src.application.dto.common import AddressDTO
from src.domain.supplier.models import Address
from src.domain.warehouse.models import DayOfWeek, OperatingHours, Warehouse
from src.domain.warehouse.services import WarehouseService


@dataclass
class OperatingHoursDTO:
    open_time: str  # HH:MM format
    close_time: str  # HH:MM format
    days_open: List[str]  # List of day names


@dataclass
class RegisterWarehouseRequest:
    name: str
    location: AddressDTO
    capacity_sqm: float
    manager_id: str
    operating_hours: OperatingHoursDTO
    warehouse_type: str = "distribution"
    phone: str = None
    email: str = None
    temperature_controlled: bool = False
    security_level: str = "standard"


@dataclass
class RegisterWarehouseResponse:
    warehouse_id: str
    status: str


class RegisterWarehouseUseCase:
    def __init__(self, warehouse_service: WarehouseService) -> None:
        self._warehouse_service = warehouse_service

    async def execute(self, request: RegisterWarehouseRequest) -> RegisterWarehouseResponse:
        address = Address(
            street=request.location.street,
            city=request.location.city,
            state=request.location.state,
            postal_code=request.location.postal_code,
            country=request.location.country,
            address_line2=request.location.address_line2,
        )

        open_time = time.fromisoformat(request.operating_hours.open_time)
        close_time = time.fromisoformat(request.operating_hours.close_time)
        days_open = [DayOfWeek(day.lower()) for day in request.operating_hours.days_open]

        operating_hours = OperatingHours(
            open_time=open_time,
            close_time=close_time,
            days_open=days_open,
        )

        warehouse = Warehouse(
            id=None,
            name=request.name,
            location=address,
            capacity_sqm=request.capacity_sqm,
            utilized_sqm=0.0,
            manager_id=request.manager_id,
            operating_hours=operating_hours,
            warehouse_type=request.warehouse_type,
            phone=request.phone,
            email=request.email,
            temperature_controlled=request.temperature_controlled,
            security_level=request.security_level,
        )

        created_warehouse = await self._warehouse_service.register_warehouse(warehouse)

        return RegisterWarehouseResponse(
            warehouse_id=created_warehouse.id,
            status="registered",
        )
