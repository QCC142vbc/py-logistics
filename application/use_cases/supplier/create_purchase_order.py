from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List

from src.domain.order.models import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from src.domain.order.services import OrderService
from src.domain.supplier.services import SupplierService


@dataclass
class PurchaseOrderItemRequest:
    item_id: str
    quantity: int
    unit_price: Decimal
    expected_delivery_date: date = None


@dataclass
class CreatePurchaseOrderRequest:
    supplier_id: str
    items: List[PurchaseOrderItemRequest]
    expected_delivery: date = None
    notes: str = None
    payment_terms: str = None


@dataclass
class CreatePurchaseOrderResponse:
    po_id: str
    status: PurchaseOrderStatus


class CreatePurchaseOrderUseCase:
    def __init__(
        self,
        order_service: OrderService,
        supplier_service: SupplierService,
    ) -> None:
        self._order_service = order_service
        self._supplier_service = supplier_service

    async def execute(self, request: CreatePurchaseOrderRequest) -> CreatePurchaseOrderResponse:
        # Validate supplier exists
        await self._supplier_service.get_supplier(request.supplier_id)

        po_items = [
            PurchaseOrderItem(
                item_id=item.item_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                expected_delivery_date=item.expected_delivery_date,
            )
            for item in request.items
        ]

        total_amount = sum(item.subtotal for item in po_items)

        purchase_order = PurchaseOrder(
            id=None,
            supplier_id=request.supplier_id,
            order_date=None,
            status=PurchaseOrderStatus.DRAFT,
            items=po_items,
            total_amount=total_amount,
            expected_delivery=request.expected_delivery,
            notes=request.notes,
            payment_terms=request.payment_terms,
        )

        created_po = await self._order_service.create_purchase_order(purchase_order)

        return CreatePurchaseOrderResponse(
            po_id=created_po.id,
            status=created_po.status,
        )
