from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from uuid import uuid4

Base = declarative_base()


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    location = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    reorder_point = Column(Integer, default=0)
    lead_time_days = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    weight_kg = Column(Float, nullable=True)
    volume_m3 = Column(Float, nullable=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class StockLevelModel(Base):
    __tablename__ = "stock_levels"

    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True)
    available = Column(Integer, default=0, nullable=False)
    reserved = Column(Integer, default=0, nullable=False)
    in_transit = Column(Integer, default=0, nullable=False)
    on_order = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)


class SupplierModel(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    contact_email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    address_street = Column(String(255), nullable=False)
    address_city = Column(String(100), nullable=False)
    address_state = Column(String(100), nullable=False)
    address_postal_code = Column(String(20), nullable=False)
    address_country = Column(String(100), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    rating = Column(Float, default=3.0, nullable=False)
    active = Column(Boolean, default=True, nullable=False, index=True)
    payment_terms = Column(String(100), nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    contact_person = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(String(255), nullable=False, index=True)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(50), nullable=False, index=True)
    total_amount = Column(Numeric(15, 2), nullable=False)
    shipping_address_street = Column(String(255), nullable=False)
    shipping_address_city = Column(String(100), nullable=False)
    shipping_address_state = Column(String(100), nullable=False)
    shipping_address_postal_code = Column(String(20), nullable=False)
    shipping_address_country = Column(String(100), nullable=False)
    billing_address_street = Column(String(255), nullable=False)
    billing_address_city = Column(String(100), nullable=False)
    billing_address_state = Column(String(100), nullable=False)
    billing_address_postal_code = Column(String(20), nullable=False)
    billing_address_country = Column(String(100), nullable=False)
    customer_name = Column(String(255), nullable=True)
    customer_email = Column(String(255), nullable=True)
    customer_phone = Column(String(50), nullable=True)
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(50), default="pending")
    shipment_id = Column(UUID(as_uuid=True), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    estimated_delivery = Column(DateTime, nullable=True)
    actual_delivery = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    discount_amount = Column(Numeric(10, 2), default=Decimal("0.00"))
    tax_amount = Column(Numeric(10, 2), default=Decimal("0.00"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    item_id = Column(String(255), nullable=False)
    sku = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)


class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    route_id = Column(UUID(as_uuid=True), nullable=True)
    carrier = Column(String(255), nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    estimated_arrival = Column(DateTime, nullable=False)
    actual_arrival = Column(DateTime, nullable=True)
    pickup_date = Column(DateTime, nullable=True)
    delivery_date = Column(DateTime, nullable=True)
    current_location_lat = Column(Float, nullable=True)
    current_location_lon = Column(Float, nullable=True)
    current_location_address = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)
    declared_value = Column(Numeric(15, 2), nullable=True)
    insurance = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)
    address_city = Column(String(100), nullable=False)
    address_state = Column(String(100), nullable=False)
    address_postal_code = Column(String(20), nullable=False)
    address_country = Column(String(100), nullable=False)
    capacity_sqm = Column(Float, nullable=False)
    utilized_sqm = Column(Float, default=0.0)
    manager_id = Column(String(255), nullable=False)
    warehouse_type = Column(String(50), default="distribution")
    active = Column(Boolean, default=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    temperature_controlled = Column(Boolean, default=False)
    security_level = Column(String(50), default="standard")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
