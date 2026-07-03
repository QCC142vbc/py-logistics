import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.database.models import Base
from src.infrastructure.database.connection import DatabaseConnection, DatabaseConfig


@pytest.fixture
async def db_session():
    """Create a test database session."""
    # Use in-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield async_session
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
def sample_item():
    """Create a sample item for testing."""
    from src.domain.inventory.models import Item
    from decimal import Decimal
    
    return Item(
        id="test-item-001",
        sku="TEST-001",
        name="Test Item",
        quantity=100,
        unit_cost=Decimal("25.00"),
        location="TEST-LOC",
        category="test",
        reorder_point=20,
        lead_time_days=7,
    )


@pytest.fixture
def sample_supplier():
    """Create a sample supplier for testing."""
    from src.domain.supplier.models import Supplier, Address
    
    return Supplier(
        id="test-supplier-001",
        name="Test Supplier",
        contact_email="test@example.com",
        phone="555-0100",
        address=Address(
            street="123 Test St",
            city="Test City",
            state="TS",
            postal_code="12345",
            country="USA",
        ),
        rating=4.0,
        active=True,
        payment_terms="NET 30",
        lead_time_days=7,
    )
