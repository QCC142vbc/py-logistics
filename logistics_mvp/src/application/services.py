from typing import Optional
from src.domain.models import Supplier, Product, Order, OrderItem


class SupplierService:
    def __init__(self, repo):
        self.repo = repo

    def create_supplier(self, name: str, email: str, phone: str) -> Supplier:
        supplier = Supplier(name=name, email=email, phone=phone)
        supplier.id = self.repo.add_supplier(supplier)
        return supplier

    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        return self.repo.get_supplier(supplier_id)


class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def create_product(self, sku: str, name: str, quantity: int, price: float) -> Product:
        product = Product(sku=sku, name=name, quantity=quantity, price=price)
        product.id = self.repo.add_product(product)
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repo.get_product(product_id)

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        return self.repo.get_product_by_sku(sku)


class OrderService:
    def __init__(self, repo, product_service):
        self.repo = repo
        self.product_service = product_service

    def create_order(self, customer_id: str, items: list[OrderItem]) -> Order:
        # Validate products exist and have stock
        for item in items:
            product = self.product_service.get_product_by_sku(item.sku)
            if not product:
                raise ValueError(f"Product {item.sku} not found")
            if product.quantity < item.quantity:
                raise ValueError(f"Insufficient stock for {item.sku}")

        # Calculate total
        total = sum(item.price * item.quantity for item in items)

        order = Order(customer_id=customer_id, items=items, total=total)
        order.id = self.repo.add_order(order)

        # Deduct stock
        for item in items:
            product = self.product_service.get_product_by_sku(item.sku)
            product.quantity -= item.quantity
            self.repo.update_product(product)

        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.repo.get_order(order_id)

    def process_order(self, order_id: int) -> Order:
        order = self.repo.get_order(order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status != "pending":
            raise ValueError("Order already processed")

        order.status = "processing"
        self.repo.update_order(order)
        return order
