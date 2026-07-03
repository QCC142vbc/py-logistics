from typing import Optional
from src.models.supplier import Supplier
from src.repositories.repository import Repository


class SupplierService:
    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_supplier(self, supplier: Supplier) -> Supplier:
        if supplier.rating < 0 or supplier.rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        
        supplier_id = await self.repo.create_supplier(supplier)
        supplier.id = supplier_id
        return supplier

    async def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        return await self.repo.get_supplier(supplier_id)

    async def list_suppliers(self) -> list[Supplier]:
        return await self.repo.list_suppliers()

    async def deactivate_supplier(self, supplier_id: str) -> Optional[Supplier]:
        supplier = await self.repo.get_supplier(supplier_id)
        if supplier:
            supplier.is_active = False
            # In a real implementation, we'd update the database
            return supplier
        return None
