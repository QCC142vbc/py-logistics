from typing import List, Optional

from src.domain.supplier.exceptions import DuplicateSupplierError, SupplierNotFoundError
from src.domain.supplier.models import Supplier, SupplierScore, SupplierContract
from src.domain.supplier.repository import SupplierRepository, SupplierFilter
from src.domain.supplier.scoring import ScoreCalculator


class SupplierService:
    def __init__(
        self,
        repository: SupplierRepository,
        score_calculator: ScoreCalculator,
    ) -> None:
        self._repository = repository
        self._score_calculator = score_calculator

    async def register_supplier(self, supplier: Supplier) -> Supplier:
        """Register a new supplier."""
        # Check if supplier with same name exists
        existing = await self._repository.get_supplier_by_name(supplier.name)
        if existing:
            raise DuplicateSupplierError(f"Supplier with name {supplier.name} already exists")

        await self._repository.save_supplier(supplier)
        return supplier

    async def get_supplier(self, supplier_id: str) -> Supplier:
        """Retrieve a supplier by ID."""
        supplier = await self._repository.get_supplier(supplier_id)
        if not supplier:
            raise SupplierNotFoundError(f"Supplier with ID {supplier_id} not found")
        return supplier

    async def update_supplier(
        self,
        supplier_id: str,
        updates: dict,
    ) -> Supplier:
        """Update supplier information."""
        supplier = await self.get_supplier(supplier_id)

        for field, value in updates.items():
            if hasattr(supplier, field):
                setattr(supplier, field, value)

        supplier.updated_at = supplier.updated_at.__class__.utcnow()
        await self._repository.save_supplier(supplier)
        return supplier

    async def evaluate_supplier(self, supplier_id: str) -> SupplierScore:
        """Evaluate a supplier's performance and calculate scores."""
        supplier = await self.get_supplier(supplier_id)

        # Calculate scores using the score calculator
        reliability_score = self._score_calculator.calculate_reliability(supplier_id)
        quality_score = self._score_calculator.calculate_quality(supplier_id)
        cost_score = self._score_calculator.calculate_cost(supplier_id)
        delivery_score = self._score_calculator.calculate_delivery(supplier_id)

        # Calculate overall score (weighted average)
        overall_score = (
            reliability_score * 0.3
            + quality_score * 0.3
            + cost_score * 0.2
            + delivery_score * 0.2
        )

        score = SupplierScore(
            supplier_id=supplier_id,
            reliability_score=reliability_score,
            quality_score=quality_score,
            cost_score=cost_score,
            delivery_score=delivery_score,
            overall_score=overall_score,
            last_calculated=supplier.updated_at.__class__.utcnow(),
            factors={
                "reliability_weight": 0.3,
                "quality_weight": 0.3,
                "cost_weight": 0.2,
                "delivery_weight": 0.2,
            },
        )

        await self._repository.update_score(score)
        
        # Update supplier rating based on overall score
        supplier.rating = overall_score / 20  # Convert 0-100 to 0-5
        await self._repository.save_supplier(supplier)

        return score

    async def get_best_suppliers_for_item(
        self,
        item_category: str,
        limit: int = 5,
    ) -> List[Supplier]:
        """Get the best suppliers for a specific item category."""
        suppliers = await self._repository.get_suppliers_by_category(item_category)
        
        # Filter active suppliers and sort by rating
        active_suppliers = [s for s in suppliers if s.active]
        sorted_suppliers = sorted(active_suppliers, key=lambda s: s.rating, reverse=True)
        
        return sorted_suppliers[:limit]

    async def deactivate_supplier(
        self,
        supplier_id: str,
        reason: str,
    ) -> None:
        """Deactivate a supplier."""
        supplier = await self.get_supplier(supplier_id)
        supplier.active = False
        supplier.notes = f"{supplier.notes or ''}\nDeactivated: {reason}" if supplier.notes else f"Deactivated: {reason}"
        await self._repository.save_supplier(supplier)

    async def activate_supplier(self, supplier_id: str) -> None:
        """Activate a supplier."""
        supplier = await self.get_supplier(supplier_id)
        supplier.active = True
        await self._repository.save_supplier(supplier)

    async def list_suppliers(
        self,
        filter: Optional[SupplierFilter] = None,
    ) -> List[Supplier]:
        """List suppliers based on filter criteria."""
        if filter is None:
            filter = SupplierFilter()
        return await self._repository.list_suppliers(filter)

    async def create_contract(self, contract: SupplierContract) -> SupplierContract:
        """Create a new supplier contract."""
        await self._repository.save_contract(contract)
        return contract

    async def get_contract(self, contract_id: str) -> SupplierContract:
        """Retrieve a contract by ID."""
        contract = await self._repository.get_contract(contract_id)
        if not contract:
            raise SupplierNotFoundError(f"Contract with ID {contract_id} not found")
        return contract

    async def get_supplier_contracts(self, supplier_id: str) -> List[SupplierContract]:
        """Retrieve all contracts for a supplier."""
        return await self._repository.get_contracts_by_supplier(supplier_id)

    async def get_expiring_contracts(
        self,
        days_threshold: int = 30,
    ) -> List[SupplierContract]:
        """Retrieve contracts expiring within the threshold."""
        return await self._repository.get_expiring_contracts(days_threshold)

    async def search_suppliers(self, query: str) -> List[Supplier]:
        """Search suppliers by name, email, or other fields."""
        return await self._repository.search_suppliers(query)
