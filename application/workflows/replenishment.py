from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from src.application.use_cases.supplier.create_purchase_order import (
    CreatePurchaseOrderRequest,
    CreatePurchaseOrderUseCase,
    PurchaseOrderItemRequest,
)
from src.domain.supplier.services import SupplierService


@dataclass
class ReplenishmentRequest:
    item_id: str
    quantity: int
    preferred_supplier_id: Optional[str] = None
    item_category: Optional[str] = None


@dataclass
class ReplenishmentResponse:
    po_id: str
    expected_delivery: date


class ReplenishmentWorkflow:
    def __init__(
        self,
        inventory_service,
        supplier_service: SupplierService,
        create_purchase_order: CreatePurchaseOrderUseCase,
    ) -> None:
        self._inventory_service = inventory_service
        self._supplier_service = supplier_service
        self._create_purchase_order = create_purchase_order

    async def execute(self, request: ReplenishmentRequest) -> ReplenishmentResponse:
        # Step 1: Get item details
        item = await self._inventory_service.get_item(request.item_id)

        # Step 2: Select supplier
        if request.preferred_supplier_id:
            supplier_id = request.preferred_supplier_id
        else:
            category = request.item_category or item.category
            best_suppliers = await self._supplier_service.get_best_suppliers_for_item(
                category,
                limit=1,
            )
            if not best_suppliers:
                raise ValueError("No suppliers available for this item")
            supplier_id = best_suppliers[0].id

        # Step 3: Create purchase order
        po_request = CreatePurchaseOrderRequest(
            supplier_id=supplier_id,
            items=[
                PurchaseOrderItemRequest(
                    item_id=request.item_id,
                    quantity=request.quantity,
                    unit_price=item.unit_cost,
                )
            ],
        )
        po_response = await self._create_purchase_order.execute(po_request)

        return ReplenishmentResponse(
            po_id=po_response.po_id,
            expected_delivery=date.today(),
        )
