from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import Base, ItemModel, SupplierModel, WarehouseModel


async def seed_suppliers(session: AsyncSession) -> None:
    """Seed sample suppliers."""
    suppliers = [
        SupplierModel(
            name="Acme Supplies Inc",
            contact_email="contact@acme.com",
            phone="555-0100",
            address_street="123 Industrial Blvd",
            address_city="Chicago",
            address_state="IL",
            address_postal_code="60601",
            address_country="USA",
            rating=4.5,
            payment_terms="NET 30",
            lead_time_days=7,
        ),
        SupplierModel(
            name="Global Logistics Partners",
            contact_email="orders@globallogistics.com",
            phone="555-0200",
            address_street="456 Shipping Way",
            address_city="Los Angeles",
            address_state="CA",
            address_postal_code="90001",
            address_country="USA",
            rating=4.2,
            payment_terms="NET 45",
            lead_time_days=10,
        ),
        SupplierModel(
            name="Prime Materials Co",
            contact_email="sales@primematerials.com",
            phone="555-0300",
            address_street="789 Manufacturing Ave",
            address_city="Houston",
            address_state="TX",
            address_postal_code="77001",
            address_country="USA",
            rating=3.8,
            payment_terms="NET 30",
            lead_time_days=5,
        ),
    ]
    
    for supplier in suppliers:
        session.add(supplier)
    
    await session.commit()


async def seed_items(session: AsyncSession) -> None:
    """Seed sample items."""
    items = [
        ItemModel(
            sku="ITEM-001",
            name="Industrial Widget A",
            quantity=100,
            unit_cost=Decimal("25.00"),
            location="WH-A-01",
            category="widgets",
            reorder_point=20,
            lead_time_days=7,
            weight_kg=2.5,
            volume_m3=0.01,
        ),
        ItemModel(
            sku="ITEM-002",
            name="Heavy Component B",
            quantity=50,
            unit_cost=Decimal("150.00"),
            location="WH-A-02",
            category="components",
            reorder_point=10,
            lead_time_days=14,
            weight_kg=25.0,
            volume_m3=0.1,
        ),
        ItemModel(
            sku="ITEM-003",
            name="Electronic Module C",
            quantity=200,
            unit_cost=Decimal("75.00"),
            location="WH-B-01",
            category="electronics",
            reorder_point=30,
            lead_time_days=5,
            weight_kg=0.5,
            volume_m3=0.005,
        ),
    ]
    
    for item in items:
        session.add(item)
    
    await session.commit()


async def seed_warehouses(session: AsyncSession) -> None:
    """Seed sample warehouses."""
    warehouses = [
        WarehouseModel(
            name="Main Distribution Center",
            address_street="100 Logistics Park",
            address_city="Atlanta",
            address_state="GA",
            address_postal_code="30301",
            address_country="USA",
            capacity_sqm=10000.0,
            utilized_sqm=3500.0,
            manager_id="MGR-001",
            warehouse_type="distribution",
            phone="555-1000",
            email="atlanta@logistics.com",
        ),
        WarehouseModel(
            name="West Coast Fulfillment",
            address_street="200 Pacific Blvd",
            address_city="Seattle",
            address_state="WA",
            address_postal_code="98101",
            address_country="USA",
            capacity_sqm=8000.0,
            utilized_sqm=4200.0,
            manager_id="MGR-002",
            warehouse_type="fulfillment",
            phone="555-2000",
            email="seattle@logistics.com",
        ),
    ]
    
    for warehouse in warehouses:
        session.add(warehouse)
    
    await session.commit()


async def seed_all(session: AsyncSession) -> None:
    """Seed all sample data."""
    await seed_suppliers(session)
    await seed_items(session)
    await seed_warehouses(session)
