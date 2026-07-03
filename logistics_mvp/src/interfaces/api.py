from fastapi import FastAPI, HTTPException
from src.domain.models import Supplier, Product, Order, OrderItem
from src.application.services import SupplierService, ProductService, OrderService
from src.infrastructure.db import get_repository

app = FastAPI(title="Logistics MVP")

repo = get_repository()
supplier_service = SupplierService(repo)
product_service = ProductService(repo)
order_service = OrderService(repo, product_service)


@app.get("/")
def root():
    return {"status": "ok"}


# Supplier endpoints
@app.post("/suppliers")
def create_supplier(name: str, email: str, phone: str):
    supplier = supplier_service.create_supplier(name, email, phone)
    return {"id": supplier.id, "name": supplier.name, "status": "created"}


@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int):
    supplier = supplier_service.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"id": supplier.id, "name": supplier.name, "email": supplier.email}


# Product endpoints
@app.post("/products")
def create_product(sku: str, name: str, quantity: int, price: float):
    product = product_service.create_product(sku, name, quantity, price)
    return {"id": product.id, "sku": product.sku, "status": "created"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "sku": product.sku, "name": product.name, "quantity": product.quantity}


# Order endpoints
@app.post("/orders")
def create_order(customer_id: str, items: list[dict]):
    order_items = [OrderItem(**item) for item in items]
    order = order_service.create_order(customer_id, order_items)
    return {"id": order.id, "customer_id": order.customer_id, "total": order.total, "status": "created"}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": order.id, "customer_id": order.customer_id, "status": order.status, "total": order.total}


@app.post("/orders/{order_id}/process")
def process_order(order_id: int):
    order = order_service.process_order(order_id)
    return {"id": order.id, "status": order.status}
