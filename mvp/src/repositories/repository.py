from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Numeric, Text, select
from typing import Optional
from datetime import datetime
from decimal import Decimal

from src.models.supplier import Supplier
from src.models.inventory import Item
from src.models.order import Order, OrderItem, OrderStatus


class Base(DeclarativeBase):
    pass


class SupplierModel(Base):
    __tablename__ = "suppliers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    location: Mapped[str] = mapped_column(String(50), default="WH-DEFAULT")
    category: Mapped[str] = mapped_column(String(100), default="general")
    reorder_point: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(50), nullable=False)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING)
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(36), nullable=False)
    item_id: Mapped[str] = mapped_column(String(36), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)


class Repository:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        return self.async_session()

    # Supplier operations
    async def create_supplier(self, supplier: Supplier) -> str:
        import uuid
        supplier_id = str(uuid.uuid4())
        db_supplier = SupplierModel(
            id=supplier_id,
            name=supplier.name,
            email=supplier.email,
            phone=supplier.phone,
            rating=supplier.rating,
            is_active=supplier.is_active,
        )
        async with self.async_session() as session:
            session.add(db_supplier)
            await session.commit()
            return supplier_id

    async def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        async with self.async_session() as session:
            result = await session.execute(
                select(SupplierModel).where(SupplierModel.id == supplier_id)
            )
            db_supplier = result.scalar_one_or_none()
            if db_supplier:
                return Supplier.model_validate(db_supplier)
            return None

    async def list_suppliers(self) -> list[Supplier]:
        async with self.async_session() as session:
            result = await session.execute(select(SupplierModel))
            return [Supplier.model_validate(s) for s in result.scalars().all()]

    # Item operations
    async def create_item(self, item: Item) -> str:
        import uuid
        item_id = str(uuid.uuid4())
        db_item = ItemModel(
            id=item_id,
            sku=item.sku,
            name=item.name,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
            location=item.location,
            category=item.category,
            reorder_point=item.reorder_point,
        )
        async with self.async_session() as session:
            session.add(db_item)
            await session.commit()
            return item_id

    async def get_item(self, item_id: str) -> Optional[Item]:
        async with self.async_session() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.id == item_id)
            )
            db_item = result.scalar_one_or_none()
            if db_item:
                return Item.model_validate(db_item)
            return None

    async def get_item_by_sku(self, sku: str) -> Optional[Item]:
        async with self.async_session() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.sku == sku)
            )
            db_item = result.scalar_one_or_none()
            if db_item:
                return Item.model_validate(db_item)
            return None

    async def update_item_quantity(self, item_id: str, quantity: int) -> Optional[Item]:
        async with self.async_session() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.id == item_id)
            )
            db_item = result.scalar_one_or_none()
            if db_item:
                db_item.quantity = quantity
                await session.commit()
                await session.refresh(db_item)
                return Item.model_validate(db_item)
            return None

    async def list_items(self) -> list[Item]:
        async with self.async_session() as session:
            result = await session.execute(select(ItemModel))
            return [Item.model_validate(i) for i in result.scalars().all()]

    # Order operations
    async def create_order(self, order: Order) -> str:
        import uuid
        order_id = str(uuid.uuid4())
        order.calculate_total()
        
        db_order = OrderModel(
            id=order_id,
            customer_id=order.customer_id,
            status=order.status,
            total_amount=order.total_amount,
            shipping_address=order.shipping_address,
        )
        
        async with self.async_session() as session:
            session.add(db_order)
            await session.flush()  # Get order_id
            
            for item in order.items:
                order_item_id = str(uuid.uuid4())
                db_order_item = OrderItemModel(
                    id=order_item_id,
                    order_id=order_id,
                    item_id=item.item_id,
                    sku=item.sku,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                session.add(db_order_item)
            
            await session.commit()
            return order_id

    async def get_order(self, order_id: str) -> Optional[Order]:
        async with self.async_session() as session:
            result = await session.execute(
                select(OrderModel).where(OrderModel.id == order_id)
            )
            db_order = result.scalar_one_or_none()
            if db_order:
                # Get order items
                items_result = await session.execute(
                    select(OrderItemModel).where(OrderItemModel.order_id == order_id)
                )
                order_items = [
                    OrderItem(
                        item_id=item.item_id,
                        sku=item.sku,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                    )
                    for item in items_result.scalars().all()
                ]
                
                return Order(
                    id=db_order.id,
                    customer_id=db_order.customer_id,
                    order_date=db_order.order_date,
                    status=OrderStatus(db_order.status),
                    items=order_items,
                    total_amount=db_order.total_amount,
                    shipping_address=db_order.shipping_address,
                    created_at=db_order.created_at,
                )
            return None

    async def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        async with self.async_session() as session:
            result = await session.execute(
                select(OrderModel).where(OrderModel.id == order_id)
            )
            db_order = result.scalar_one_or_none()
            if db_order:
                db_order.status = status.value
                await session.commit()
                await session.refresh(db_order)
                return await self.get_order(order_id)
            return None

    async def list_orders(self) -> list[Order]:
        async with self.async_session() as session:
            result = await session.execute(select(OrderModel))
            orders = []
            for db_order in result.scalars().all():
                order = await self.get_order(db_order.id)
                if order:
                    orders.append(order)
            return orders


# Global repository instance
_repository: Optional[Repository] = None


def get_repository() -> Repository:
    global _repository
    if _repository is None:
        from src.config import settings
        _repository = Repository(settings.database_url)
    return _repository
