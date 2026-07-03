import pytest
from src.models.supplier import Supplier
from src.models.inventory import Item
from src.services.supplier_service import SupplierService
from src.services.inventory_service import InventoryService
from src.repositories.repository import Repository


@pytest.mark.asyncio
async def test_create_supplier():
    repo = Repository("sqlite+aiosqlite:///:memory:")
    await repo.create_tables()
    
    service = SupplierService(repo)
    supplier = Supplier(
        name="Test Supplier",
        email="test@example.com",
        phone="555-0100",
        rating=4.5,
    )
    
    result = await service.create_supplier(supplier)
    assert result.id is not None
    assert result.name == "Test Supplier"


@pytest.mark.asyncio
async def test_create_item():
    repo = Repository("sqlite+aiosqlite:///:memory:")
    await repo.create_tables()
    
    service = InventoryService(repo)
    item = Item(
        sku="TEST-001",
        name="Test Item",
        quantity=100,
        unit_cost=25.00,
        location="WH-A-01",
    )
    
    result = await service.create_item(item)
    assert result.id is not None
    assert result.sku == "TEST-001"
    assert result.quantity == 100


@pytest.mark.asyncio
async def test_adjust_stock():
    repo = Repository("sqlite+aiosqlite:///:memory:")
    await repo.create_tables()
    
    service = InventoryService(repo)
    item = Item(
        sku="TEST-001",
        name="Test Item",
        quantity=100,
        unit_cost=25.00,
    )
    created = await service.create_item(item)
    
    updated = await service.adjust_stock(created.id, -10)
    assert updated.quantity == 90
    
    updated = await service.adjust_stock(created.id, 5)
    assert updated.quantity == 95


@pytest.mark.asyncio
async def test_low_stock_detection():
    repo = Repository("sqlite+aiosqlite:///:memory:")
    await repo.create_tables()
    
    service = InventoryService(repo)
    item = Item(
        sku="TEST-001",
        name="Test Item",
        quantity=5,
        unit_cost=25.00,
        reorder_point=10,
    )
    await service.create_item(item)
    
    low_stock = await service.get_low_stock_items()
    assert len(low_stock) == 1
    assert low_stock[0].sku == "TEST-001"
