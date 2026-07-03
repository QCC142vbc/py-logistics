from fastapi import APIRouter, Depends, HTTPException
from src.models.supplier import Supplier
from src.models.inventory import Item
from src.models.order import Order, OrderItem
from src.services.supplier_service import SupplierService
from src.services.inventory_service import InventoryService
from src.services.order_service import OrderService
from src.repositories.repository import get_repository

router = APIRouter(prefix="/api/v1")


# Supplier routes
@router.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier: Supplier):
    service = SupplierService(get_repository())
    return await service.create_supplier(supplier)


@router.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier(supplier_id: str):
    service = SupplierService(get_repository())
    supplier = await service.get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.get("/suppliers", response_model=list[Supplier])
async def list_suppliers():
    service = SupplierService(get_repository())
    return await service.list_suppliers()


# Inventory routes
@router.post("/items", response_model=Item)
async def create_item(item: Item):
    service = InventoryService(get_repository())
    return await service.create_item(item)


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    service = InventoryService(get_repository())
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items", response_model=list[Item])
async def list_items():
    service = InventoryService(get_repository())
    return await service.list_items()


@router.get("/items/low-stock", response_model=list[Item])
async def get_low_stock_items():
    service = InventoryService(get_repository())
    return await service.get_low_stock_items()


@router.patch("/items/{item_id}/stock")
async def adjust_stock(item_id: str, quantity_change: int):
    service = InventoryService(get_repository())
    item = await service.adjust_stock(item_id, quantity_change)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "new_quantity": item.quantity}


# Order routes
@router.post("/orders", response_model=Order)
async def create_order(order: Order):
    repo = get_repository()
    inventory_service = InventoryService(repo)
    order_service = OrderService(repo, inventory_service)
    return await order_service.create_order(order)


@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    repo = get_repository()
    inventory_service = InventoryService(repo)
    order_service = OrderService(repo, inventory_service)
    order = await order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/orders", response_model=list[Order])
async def list_orders():
    repo = get_repository()
    inventory_service = InventoryService(repo)
    order_service = OrderService(repo, inventory_service)
    return await order_service.list_orders()


@router.post("/orders/{order_id}/process", response_model=Order)
async def process_order(order_id: str):
    repo = get_repository()
    inventory_service = InventoryService(repo)
    order_service = OrderService(repo, inventory_service)
    return await order_service.process_order(order_id)


@router.post("/orders/{order_id}/cancel", response_model=Order)
async def cancel_order(order_id: str):
    repo = get_repository()
    inventory_service = InventoryService(repo)
    order_service = OrderService(repo, inventory_service)
    return await order_service.cancel_order(order_id)
