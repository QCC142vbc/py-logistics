from dataclasses import dataclass
from decimal import Decimal
from typing import List

from src.domain.order.models import Order, OrderItem


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]


@dataclass
class PaymentInfo:
    payment_method: str
    card_last_four: Optional[str] = None
    transaction_id: Optional[str] = None


class OrderValidator:
    def __init__(self) -> None:
        pass

    def validate_order(self, order: Order) -> ValidationResult:
        """Validate an order."""
        errors: List[str] = []

        # Validate customer
        if not order.customer_id:
            errors.append("Customer ID is required")

        # Validate items
        if not order.items:
            errors.append("Order must have at least one item")
        else:
            for idx, item in enumerate(order.items):
                item_errors = self._validate_order_item(item)
                for error in item_errors:
                    errors.append(f"Item {idx}: {error}")

        # Validate addresses
        if not order.shipping_address:
            errors.append("Shipping address is required")
        if not order.billing_address:
            errors.append("Billing address is required")

        # Validate total amount
        calculated_total = order.calculate_total()
        if abs(calculated_total - order.total_amount) > Decimal("0.01"):
            errors.append(
                f"Total amount mismatch. Expected: {calculated_total}, Got: {order.total_amount}"
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _validate_order_item(self, item: OrderItem) -> List[str]:
        """Validate an order item."""
        errors: List[str] = []

        if not item.item_id:
            errors.append("Item ID is required")
        if not item.sku:
            errors.append("SKU is required")
        if item.quantity <= 0:
            errors.append("Quantity must be positive")
        if item.unit_price <= 0:
            errors.append("Unit price must be positive")

        return errors

    def validate_payment_method(self, payment_info: PaymentInfo) -> ValidationResult:
        """Validate payment information."""
        errors: List[str] = []

        if not payment_info.payment_method:
            errors.append("Payment method is required")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    def validate_items_availability(
        self,
        items: List[OrderItem],
        available_quantities: dict[str, int],
    ) -> bool:
        """Validate if all items are available in sufficient quantity."""
        for item in items:
            available = available_quantities.get(item.item_id, 0)
            if available < item.quantity:
                return False
        return True
