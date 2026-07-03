from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from src.domain.supplier.models import Supplier, SupplierScore, SupplierContract


@dataclass
class SupplierFilter:
    name: Optional[str] = None
    category: Optional[str] = None
    active_only: bool = True
    min_rating: Optional[float] = None
    country: Optional[str] = None


class SupplierRepository(ABC):
    @abstractmethod
    async def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        """Retrieve a supplier by ID."""
        pass

    @abstractmethod
    async def get_supplier_by_name(self, name: str) -> Optional[Supplier]:
        """Retrieve a supplier by name."""
        pass

    @abstractmethod
    async def save_supplier(self, supplier: Supplier) -> None:
        """Save or update a supplier."""
        pass

    @abstractmethod
    async def delete_supplier(self, supplier_id: str) -> None:
        """Delete a supplier by ID."""
        pass

    @abstractmethod
    async def list_suppliers(self, filter: SupplierFilter) -> List[Supplier]:
        """List suppliers based on filter criteria."""
        pass

    @abstractmethod
    async def get_active_suppliers(self) -> List[Supplier]:
        """Retrieve all active suppliers."""
        pass

    @abstractmethod
    async def update_score(self, score: SupplierScore) -> None:
        """Update or create a supplier score."""
        pass

    @abstractmethod
    async def get_score(self, supplier_id: str) -> Optional[SupplierScore]:
        """Retrieve the current score for a supplier."""
        pass

    @abstractmethod
    async def save_contract(self, contract: SupplierContract) -> None:
        """Save or update a supplier contract."""
        pass

    @abstractmethod
    async def get_contract(self, contract_id: str) -> Optional[SupplierContract]:
        """Retrieve a contract by ID."""
        pass

    @abstractmethod
    async def get_contracts_by_supplier(self, supplier_id: str) -> List[SupplierContract]:
        """Retrieve all contracts for a supplier."""
        pass

    @abstractmethod
    async def get_active_contracts(self) -> List[SupplierContract]:
        """Retrieve all active contracts."""
        pass

    @abstractmethod
    async def get_expiring_contracts(self, days_threshold: int = 30) -> List[SupplierContract]:
        """Retrieve contracts expiring within the threshold."""
        pass

    @abstractmethod
    async def get_suppliers_by_category(self, category: str) -> List[Supplier]:
        """Retrieve all suppliers that supply a specific category."""
        pass

    @abstractmethod
    async def search_suppliers(self, query: str) -> List[Supplier]:
        """Search suppliers by name, email, or other fields."""
        pass
