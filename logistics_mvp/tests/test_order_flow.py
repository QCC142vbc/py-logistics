from src.infrastructure.db import Repository
from src.application.services import SupplierService, ProductService, OrderService
from src.domain.models import OrderItem


def test_order_flow():
    repo = Repository(":memory:")  # In-memory SQLite for testing
    supplier_service = SupplierService(repo)
    product_service = ProductService(repo)
    order_service = OrderService(repo, product_service)

    # 1. Create supplier
    supplier = supplier_service.create_supplier("Acme Supplies", "acme@example.com", "555-0100")
    assert supplier.id is not None
    print(f"✓ Created supplier: {supplier.name} (ID: {supplier.id})")

    # 2. Create product
    product = product_service.create_product("WIDGET-001", "Widget A", 100, 25.00)
    assert product.id is not None
    print(f"✓ Created product: {product.name} (SKU: {product.sku}, Qty: {product.quantity})")

    # 3. Create order
    items = [OrderItem(product_id=product.id, sku="WIDGET-001", quantity=10, price=25.00)]
    order = order_service.create_order("CUST-001", items)
    assert order.id is not None
    assert order.total == 250.00
    print(f"✓ Created order: ID {order.id}, Total: ${order.total}")

    # 4. Verify stock deducted
    updated_product = product_service.get_product(product.id)
    assert updated_product.quantity == 90
    print(f"✓ Stock deducted: {updated_product.quantity} remaining")

    # 5. Process order
    processed_order = order_service.process_order(order.id)
    assert processed_order.status == "processing"
    print(f"✓ Order processed: Status {processed_order.status}")

    print("\n✅ Full flow test passed!")


if __name__ == "__main__":
    test_order_flow()
