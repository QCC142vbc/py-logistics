from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from src.domain.warehouse.models import Warehouse, StorageLocation, WarehouseTransfer, TransferStatus


@dataclass
class WarehouseFilter:
    name: Optional[str] = None
    warehouse_type: Optional[str] = None
    active_only: bool = True
    manager_id: Optional[str] = None
    country: Optional[str] = None


@dataclass
class StorageLocationFilter:
    warehouse_id: str
    zone: Optional[str] = None
    item_type: Optional[str] = None
    temperature_controlled: Optional[bool] = None
    has_capacity: bool = False


@dataclass
class TransferFilter:
    from_warehouse_id: Optional[str] = None
    to_warehouse_id: Optional[str] = None
    status: Optional[TransferStatus] = None
    initiated_by: Optional[str] = None


class WarehouseRepository(ABC):
    @abstractmethod
    async def get_warehouse(self, warehouse_id: str) -> Optional[Warehouse]:
        """Retrieve a warehouse by ID."""
        pass

    @abstractmethod
    async def save_warehouse(self, warehouse: Warehouse) -> None:
        """Save or update a warehouse."""
        pass

    @abstractmethod
    async def delete_warehouse(self, warehouse_id: str) -> None:
        """Delete a warehouse by ID."""
        pass

    @abstractmethod
    async def list_warehouses(self, filter: WarehouseFilter) -> List[Warehouse]:
        """List warehouses based on filter criteria."""
        pass

    @abstractmethod
    async def get_active_warehouses(self) -> List[Warehouse]:
        """Retrieve all active warehouses."""
        pass

    @abstractmethod
    async def get_storage_location(self, location_id: str) -> Optional[StorageLocation]:
        """Retrieve a storage location by ID."""
        pass

    @abstractmethod
    async def save_storage_location(self, location: StorageLocation) -> None:
        """Save or update a storage location."""
        pass

    @abstractmethod
    async def delete_storage_location(self, location_id: str) -> None:
        """Delete a storage location by ID."""
        pass

    @abstractmethod
    async def find_available_storage(
        self,
        warehouse_id: str,
        item_type: str,
        required_units: int,
        temperature_controlled: bool = False,
    ) -> Optional[StorageLocation]:
        """Find an available storage location with sufficient capacity."""
        pass

    @abstractmethod
    async def list_storage_locations(
        self,
        filter: StorageLocationFilter,
    ) -> List[StorageLocation]:
        """List storage locations based on filter criteria."""
        pass

    @abstractmethod
    async def get_storage_locations_by_warehouse(
        self,
        warehouse_id: str,
    ) -> List[StorageLocation]:
        """Retrieve all storage locations for a warehouse."""
        pass

    @abstractmethod
    async def save_transfer(self, transfer: WarehouseTransfer) -> None:
        """Save or update a warehouse transfer."""
        pass

    @abstractmethod
    async def get_transfer(self, transfer_id: str) -> Optional[WarehouseTransfer]:
        """Retrieve a transfer by ID."""
        pass

    @abstractmethod
    async def delete_transfer(self, transfer_id: str) -> None:
        """Delete a transfer by ID."""
        pass

    @abstractmethod
    async def list_transfers(self, filter: TransferFilter) -> List[WarehouseTransfer]:
        """List transfers based on filter criteria."""
        pass

    @abstractmethod
    async def get_transfers_by_warehouse(
        self,
        warehouse_id: str,
    ) -> List[WarehouseTransfer]:
        """Retrieve all transfers involving a warehouse."""
        pass

    @abstractmethod
    async def get_pending_transfers(self) -> List[WarehouseTransfer]:
        """Retrieve all pending transfers."""
        pass

    @abstractmethod
    async def get_in_transit_transfers(self) -> List[WarehouseTransfer]:
        """Retrieve all in-transit transfers."""
        pass

    @abstractmethod
    async def search_warehouses(self, query: str) -> List[Warehouse]:
        """Search warehouses by name or location."""
        pass
