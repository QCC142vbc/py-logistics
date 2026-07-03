from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.domain.inventory.exceptions import InsufficientStockError
from src.domain.inventory.services import InventoryService
from src.domain.warehouse.exceptions import (
    InsufficientCapacityError,
    StorageLocationNotFoundError,
    WarehouseNotFoundError,
)
from src.domain.warehouse.models import (
    StorageLocation,
    StorageRecommendation,
    TransferItem,
    Warehouse,
    WarehouseTransfer,
    TransferStatus,
)
from src.domain.warehouse.repository import (
    StorageLocationFilter,
    TransferFilter,
    WarehouseFilter,
    WarehouseRepository,
)


@dataclass
class StorageRecommendation:
    location_id: str
    location_code: str
    current_utilization: float
    recommended_action: str  # move, consolidate, expand
    estimated_savings: Optional[float] = None


class WarehouseService:
    def __init__(
        self,
        repo: WarehouseRepository,
        inventory_service: InventoryService,
    ) -> None:
        self._repo = repo
        self._inventory_service = inventory_service

    async def register_warehouse(self, warehouse: Warehouse) -> Warehouse:
        """Register a new warehouse."""
        await self._repo.save_warehouse(warehouse)
        return warehouse

    async def get_warehouse(self, warehouse_id: str) -> Warehouse:
        """Retrieve a warehouse by ID."""
        warehouse = await self._repo.get_warehouse(warehouse_id)
        if not warehouse:
            raise WarehouseNotFoundError(f"Warehouse with ID {warehouse_id} not found")
        return warehouse

    async def update_warehouse(
        self,
        warehouse_id: str,
        updates: dict,
    ) -> Warehouse:
        """Update warehouse information."""
        warehouse = await self.get_warehouse(warehouse_id)

        for field, value in updates.items():
            if hasattr(warehouse, field):
                setattr(warehouse, field, value)

        warehouse.updated_at = warehouse.updated_at.__class__.utcnow()
        await self._repo.save_warehouse(warehouse)
        return warehouse

    async def allocate_storage(
        self,
        item_id: str,
        warehouse_id: str,
        quantity: int,
        item_type: str,
        temperature_controlled: bool = False,
    ) -> StorageLocation:
        """Allocate storage for an item in a warehouse."""
        # Find available storage location
        location = await self._repo.find_available_storage(
            warehouse_id,
            item_type,
            quantity,
            temperature_controlled,
        )

        if not location:
            raise InsufficientCapacityError(
                f"No available storage for {quantity} units of type {item_type}"
            )

        # Update location with new items
        location.current_units += quantity
        await self._repo.save_storage_location(location)

        return location

    async def deallocate_storage(
        self,
        location_id: str,
        quantity: int,
    ) -> StorageLocation:
        """Remove items from a storage location."""
        location = await self._repo.get_storage_location(location_id)
        if not location:
            raise StorageLocationNotFoundError(f"Storage location {location_id} not found")

        if location.current_units < quantity:
            raise InsufficientCapacityError(
                f"Cannot remove {quantity} units. Current: {location.current_units}"
            )

        location.current_units -= quantity
        await self._repo.save_storage_location(location)
        return location

    async def initiate_transfer(
        self,
        transfer: WarehouseTransfer,
    ) -> WarehouseTransfer:
        """Initiate a warehouse transfer."""
        # Validate warehouses exist
        await self.get_warehouse(transfer.from_warehouse_id)
        await self.get_warehouse(transfer.to_warehouse_id)

        # Validate items are available at source
        for item in transfer.items:
            stock_level = await self._inventory_service.get_stock_level(item.item_id)
            if stock_level.available < item.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for item {item.item_id} at source warehouse"
                )

        transfer.status = TransferStatus.PENDING
        await self._repo.save_transfer(transfer)
        return transfer

    async def approve_transfer(
        self,
        transfer_id: str,
        approved_by: str,
    ) -> WarehouseTransfer:
        """Approve a warehouse transfer."""
        transfer = await self._repo.get_transfer(transfer_id)
        if not transfer:
            raise WarehouseNotFoundError(f"Transfer with ID {transfer_id} not found")

        if not transfer.can_be_approved:
            raise WarehouseNotFoundError(
                f"Transfer cannot be approved in current state: {transfer.status}"
            )

        transfer.status = TransferStatus.APPROVED
        transfer.approved_by = approved_by
        transfer.approved_at = datetime.utcnow()
        await self._repo.save_transfer(transfer)
        return transfer

    async def start_transfer(
        self,
        transfer_id: str,
        shipment_id: str,
    ) -> WarehouseTransfer:
        """Mark a transfer as in transit."""
        transfer = await self._repo.get_transfer(transfer_id)
        if not transfer:
            raise WarehouseNotFoundError(f"Transfer with ID {transfer_id} not found")

        transfer.status = TransferStatus.IN_TRANSIT
        transfer.shipment_id = shipment_id
        await self._repo.save_transfer(transfer)
        return transfer

    async def complete_transfer(
        self,
        transfer_id: str,
        received_by: str,
    ) -> WarehouseTransfer:
        """Complete a warehouse transfer by receiving items."""
        transfer = await self._repo.get_transfer(transfer_id)
        if not transfer:
            raise WarehouseNotFoundError(f"Transfer with ID {transfer_id} not found")

        transfer.status = TransferStatus.RECEIVED
        transfer.received_by = received_by
        transfer.received_at = datetime.utcnow()
        await self._repo.save_transfer(transfer)
        return transfer

    async def cancel_transfer(
        self,
        transfer_id: str,
        reason: str,
    ) -> WarehouseTransfer:
        """Cancel a warehouse transfer."""
        transfer = await self._repo.get_transfer(transfer_id)
        if not transfer:
            raise WarehouseNotFoundError(f"Transfer with ID {transfer_id} not found")

        if not transfer.can_be_cancelled:
            raise WarehouseNotFoundError(
                f"Transfer cannot be cancelled in current state: {transfer.status}"
            )

        transfer.status = TransferStatus.CANCELLED
        transfer.notes = f"{transfer.notes or ''}\nCancelled: {reason}"
        await self._repo.save_transfer(transfer)
        return transfer

    async def get_warehouse_utilization(self, warehouse_id: str) -> float:
        """Get the current utilization percentage of a warehouse."""
        warehouse = await self.get_warehouse(warehouse_id)
        return warehouse.utilization_percentage

    async def optimize_storage_layout(
        self,
        warehouse_id: str,
    ) -> List[StorageRecommendation]:
        """Generate storage optimization recommendations for a warehouse."""
        locations = await self._repo.get_storage_locations_by_warehouse(warehouse_id)
        
        recommendations: List[StorageRecommendation] = []
        
        for location in locations:
            utilization = location.utilization_percentage
            
            if utilization < 20:
                recommendations.append(
                    StorageRecommendation(
                        location_id=location.location_id,
                        location_code=location.location_code,
                        current_utilization=utilization,
                        recommended_action="consolidate",
                        estimated_savings=location.capacity_units * 0.1,
                    )
                )
            elif utilization > 90:
                recommendations.append(
                    StorageRecommendation(
                        location_id=location.location_id,
                        location_code=location.location_code,
                        current_utilization=utilization,
                        recommended_action="expand",
                    )
                )
        
        return recommendations

    async def list_warehouses(
        self,
        filter: Optional[WarehouseFilter] = None,
    ) -> List[Warehouse]:
        """List warehouses based on filter criteria."""
        if filter is None:
            filter = WarehouseFilter()
        return await self._repo.list_warehouses(filter)

    async def list_storage_locations(
        self,
        filter: StorageLocationFilter,
    ) -> List[StorageLocation]:
        """List storage locations based on filter criteria."""
        return await self._repo.list_storage_locations(filter)

    async def list_transfers(
        self,
        filter: Optional[TransferFilter] = None,
    ) -> List[WarehouseTransfer]:
        """List transfers based on filter criteria."""
        if filter is None:
            filter = TransferFilter()
        return await self._repo.list_transfers(filter)

    async def get_warehouses_near_capacity(self, threshold: float = 0.9) -> List[Warehouse]:
        """Get warehouses that are near or at capacity."""
        warehouses = await self._repo.get_active_warehouses()
        return [w for w in warehouses if w.is_near_capacity(threshold)]
