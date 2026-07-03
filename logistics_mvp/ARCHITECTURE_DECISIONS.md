# Architecture Decisions - Logistics MVP

## Overview

This document explains **why** the MVP was built this way, **where** each decision was made, and the **context** behind simplifying the original 10,000-line enterprise system into a functional 300-line MVP.

---

## Problem Statement

### Original System Issues

The original logistics system had these problems:

1. **Too Many Layers** - 7+ layers (API → use case → DTO → service → domain → repository → database)
   - **Where**: `src/domain/`, `src/application/`, `src/infrastructure/`, `src/interfaces/`
   - **Why it's a problem**: Tracing a single request requires jumping through 7 files. Debugging is painful.

2. **Premature Optimization** - RabbitMQ, Redis, S3, event dispatchers
   - **Where**: `src/infrastructure/messaging/`, `src/infrastructure/cache/`, `src/domain/events/`
   - **Why it's a problem**: These add complexity without proven need. A basic logistics system doesn't need message queues.

3. **Over-Abstraction** - Repository pattern interfaces, factory methods, value objects
   - **Where**: `src/domain/*/repository.py`, `src/domain/common/models.py`
   - **Why it's a problem**: Abstracting everything before knowing if it's needed creates cognitive overhead.

4. **Unused Features** - Simulation engine, forecasting, optimization
   - **Where**: `src/simulation/`, `src/analytics/`
   - **Why it's a problem**: These are nice-to-have features that block getting core functionality working.

---

## MVP Design Decisions

### Decision 1: Use SQLite Instead of PostgreSQL

**Where**: `src/infrastructure/db.py`

**Why**:
- Zero setup - no database server to install
- File-based - easy to delete and recreate
- Sufficient for MVP scale
- Can migrate to PostgreSQL later if needed

**Trade-off**:
- ❌ Not suitable for high concurrency
- ✅ Perfect for single-user development

**Code**:
```python
class Repository:
    def __init__(self, db_path: str = "logistics.db"):
        self.db_path = db_path
        self._init_db()
```

---

### Decision 2: Use Dataclasses Instead of Pydantic

**Where**: `src/domain/models.py`

**Why**:
- Built into Python 3.7+ (no dependency)
- Simpler syntax
- Less validation overhead
- Good enough for internal data structures

**Trade-off**:
- ❌ No automatic validation
- ✅ Less boilerplate, faster to write

**Code**:
```python
@dataclass
class Supplier:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""
```

---

### Decision 3: Direct SQL Instead of ORM

**Where**: `src/infrastructure/db.py`

**Why**:
- No SQLAlchemy dependency
- Explicit queries are easier to understand
- Less magic, more control
- Faster to debug

**Trade-off**:
- ❌ Manual SQL writing
- ✅ Clear what's happening, no hidden behavior

**Code**:
```python
def add_supplier(self, supplier: Supplier) -> int:
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO suppliers (name, email, phone) VALUES (?, ?, ?)",
        (supplier.name, supplier.email, supplier.phone)
    )
```

---

### Decision 4: 4-Layer Architecture Instead of 7

**Where**: Entire project structure

**Why**:
- **Models** (`src/domain/models.py`) - Data structures
- **Services** (`src/application/services.py`) - Business logic
- **Repository** (`src/infrastructure/db.py`) - Data access
- **API** (`src/interfaces/api.py`) - HTTP interface

**Trade-off**:
- ❌ Less separation of concerns
- ✅ Easier to trace and debug

**Data Flow**:
```
API (FastAPI)
  ↓
Service (business logic)
  ↓
Repository (SQL operations)
  ↓
SQLite (database)
```

---

### Decision 5: No Event-Driven Architecture

**Where**: Not implemented (removed from original)

**Why**:
- Events add complexity (handlers, dispatchers, subscribers)
- Not needed for synchronous operations
- Can add later if async processing is needed

**Trade-off**:
- ❌ No loose coupling between modules
- ✅ Simpler call chain, easier to understand

**Original (removed)**:
```python
# src/domain/events/dispatcher.py
class EventDispatcher:
    def publish(self, event):
        for handler in self.handlers[event.__class__]:
            handler.handle(event)
```

---

### Decision 6: No Caching Layer

**Where**: Not implemented (removed from original)

**Why**:
- SQLite is fast enough for MVP
- Caching adds invalidation complexity
- Can add Redis later if performance is an issue

**Trade-off**:
- ❌ No performance optimization
- ✅ One less moving part to debug

---

### Decision 7: No Message Queue

**Where**: Not implemented (removed from original)

**Why**:
- Orders can be processed synchronously
- RabbitMQ adds infrastructure overhead
- Background tasks can use simple threading if needed

**Trade-off**:
- ❌ No async processing
- ✅ Simpler deployment

---

### Decision 8: Global Repository Instance

**Where**: `src/infrastructure/db.py`

**Why**:
- Simple dependency injection
- No need for DI framework
- Easy to swap for testing

**Trade-off**:
- ❌ Global state
- ✅ Minimal boilerplate

**Code**:
```python
_repo: Optional[Repository] = None

def get_repository() -> Repository:
    global _repo
    if _repo is None:
        _repo = Repository()
    return _repo
```

---

### Decision 9: Simple Service Layer

**Where**: `src/application/services.py`

**Why**:
- Combines use cases and domain services
- One class per domain (Supplier, Product, Order)
- Clear separation of business logic from data access

**Trade-off**:
- ❌ Less granular use cases
- ✅ Easier to find related logic

**Code**:
```python
class SupplierService:
    def __init__(self, repo):
        self.repo = repo

    def create_supplier(self, name: str, email: str, phone: str) -> Supplier:
        supplier = Supplier(name=name, email=email, phone=phone)
        supplier.id = self.repo.add_supplier(supplier)
        return supplier
```

---

### Decision 10: Minimal API Endpoints

**Where**: `src/interfaces/api.py`

**Why**:
- One endpoint per operation (create, get, process)
- No complex query parameters
- No pagination (not needed yet)
- No authentication (not needed yet)

**Trade-off**:
- ❌ Less feature-rich
- ✅ Clear and simple

**Code**:
```python
@app.post("/suppliers")
def create_supplier(name: str, email: str, phone: str):
    supplier = supplier_service.create_supplier(name, email, phone)
    return {"id": supplier.id, "name": supplier.name, "status": "created"}
```

---

## File-by-File Explanation with Line Numbers

### `src/domain/models.py` (41 lines)

**Purpose**: Define data structures

**Format**: Python dataclasses (lines 5-41)

**Why dataclasses**:
- **Line 1**: `from dataclasses import dataclass` - Built-in Python 3.7+, no external dependency
- **Line 2**: `from typing import Optional` - Type hints for optional fields
- **Lines 5-10**: `@dataclass class Supplier` - Simple data container with id, name, email, phone
  - Line 7: `id: Optional[int] = None` - Optional because assigned by database
  - Lines 8-10: String fields with empty defaults for flexibility
- **Lines 13-19**: `@dataclass class Product` - Inventory items with stock tracking
  - Line 16: `sku: str = ""` - Stock keeping unit for product identification
  - Line 18: `quantity: int = 0` - Current stock level
  - Line 19: `price: float = 0.0` - Unit price as float (simple, not Decimal)
- **Lines 22-27**: `@dataclass class OrderItem` - Line items in orders
  - Line 24: `product_id: int` - References product in database
  - Line 25: `sku: str` - Stored for reference even if product changes
  - Lines 26-27: Quantity and price at time of order
- **Lines 30-41**: `@dataclass class Order` - Customer order with items
  - Line 34: `items: list[OrderItem] = None` - List of order items
  - Lines 38-40: `__post_init__` - Initialize empty list if None (dataclass pattern)

**What's NOT included**:
- Value objects (SKU, Quantity, Location) - Too much abstraction for MVP
- Base entity class - Not needed, simple dataclasses suffice
- Validation logic - Moved to services layer
- Pydantic models - Added dependency without clear benefit
- Decimal for price - Float is simpler for MVP

---

### `src/application/services.py` (75 lines)

**Purpose**: Business logic layer

**Format**: Service classes with business rules (lines 5-75)

**Why services**:
- **Line 1**: `from typing import Optional` - Type hints for return values
- **Line 2**: Import domain models - Direct dependency, no DTOs
- **Lines 5-16**: `class SupplierService` - Supplier business logic
  - Line 6: `__init__(self, repo)` - Dependency injection of repository
  - Line 7: Store repo as instance variable
  - Lines 9-12: `create_supplier()` - Create supplier and assign ID from DB
  - Lines 14-15: `get_supplier()` - Simple retrieval, no business rules needed
- **Lines 18-32**: `class ProductService` - Product business logic
  - Lines 22-25: `create_product()` - Create product with SKU, name, quantity, price
  - Lines 27-28: `get_product()` - Retrieve by ID
  - Lines 30-31: `get_product_by_sku()` - Retrieve by SKU (important for order validation)
- **Lines 34-75**: `class OrderService` - Order business logic with stock validation
  - Line 35: `__init__(self, repo, product_service)` - Depends on both repo and product service
  - Lines 39-46: `create_order()` - Core business logic:
    - Lines 41-46: Validate each item exists and has sufficient stock
    - Line 44: Raise ValueError if product not found
    - Line 45: Raise ValueError if insufficient stock
    - Line 49: Calculate total price
    - Line 51: Create order object
    - Line 52: Save to database
    - Lines 54-58: Deduct stock for each item (atomic operation in real system)
  - Lines 62-63: `get_order()` - Simple retrieval
  - Lines 65-74: `process_order()` - Change order status
    - Lines 67-68: Validate order exists
    - Lines 69-70: Validate order is in pending state
    - Line 72: Change status to processing
    - Line 73: Update in database

**What's NOT included**:
- DTOs (Data Transfer Objects) - Use domain models directly
- Workflows - Keep it simple, one method per operation
- Event publishing - No event-driven architecture
- Transaction management - SQLite handles basic transactions

---

### `src/infrastructure/db.py` (182 lines)

**Purpose**: Data access layer

**Format**: Repository class with direct SQL operations (lines 6-182)

**Why SQLite**:
- **Line 1**: `import sqlite3` - Built-in Python library, no installation needed
- **Line 2**: `from typing import Optional, List` - Type hints
- **Line 3**: Import domain models - Direct dependency, no ORM mapping
- **Lines 6-9**: `class Repository.__init__()` - Initialize with db_path
  - Line 7: Accept db_path parameter (default: "logistics.db")
  - Line 8: Store db_path
  - Line 9: Call `_init_db()` to create tables
- **Lines 11-56**: `_init_db()` - Create database tables
  - Line 12: Connect to SQLite database
  - Lines 15-22: Create suppliers table with id, name, email, phone
  - Lines 24-32: Create products table with id, sku (unique), name, quantity, price
  - Lines 34-41: Create orders table with id, customer_id, status, total
  - Lines 43-53: Create order_items table with foreign key to orders
  - Lines 55-56: Commit and close connection
- **Lines 58-79**: Supplier operations
  - Lines 59-69: `add_supplier()` - Insert supplier and return ID
    - Line 66: Get last inserted row ID
  - Lines 71-79: `get_supplier()` - Retrieve supplier by ID
    - Line 74: Execute SELECT query
    - Line 75: Fetch single row
    - Lines 78: Convert to Supplier dataclass
- **Lines 81-122**: Product operations
  - Lines 82-92: `add_product()` - Insert product and return ID
  - Lines 94-102: `get_product()` - Retrieve product by ID
  - Lines 104-112: `get_product_by_sku()` - Retrieve product by SKU (important for orders)
  - Lines 114-122: `update_product()` - Update product quantity
    - Line 118: Update quantity field
- **Lines 124-170**: Order operations
  - Lines 125-142: `add_order()` - Insert order and order items
    - Line 132: Get order ID
    - Lines 134-138: Insert each order item
  - Lines 144-160: `get_order()` - Retrieve order with items
    - Lines 147-148: Get order data
    - Lines 154-157: Get order items
    - Line 157: Convert to OrderItem list
  - Lines 162-170: `update_order()` - Update order status
- **Lines 173-182**: Global repository pattern
  - Line 174: Global variable for singleton
  - Lines 177-181: `get_repository()` - Return singleton instance

**What's NOT included**:
- ORM (SQLAlchemy) - Direct SQL is clearer and simpler
- Connection pooling - Not needed for SQLite
- Migration system - Recreate DB for now, add Alembic later
- Async operations - SQLite doesn't support async well
- Context managers - Simple open/close for clarity

---

### `src/interfaces/api.py` (69 lines)

**Purpose**: HTTP API layer

**Format**: FastAPI application with route handlers (lines 1-69)

**Why FastAPI**:
- **Line 1**: `from fastapi import FastAPI, HTTPException` - Modern async web framework
- **Line 2**: Import domain models - Direct dependency, no request DTOs
- **Line 3**: Import services - Business logic layer
- **Line 4**: Import repository - Data access layer
- **Line 6**: `app = FastAPI(title="Logistics MVP")` - Create FastAPI app instance
- **Lines 8-11**: Global service instances
  - Line 8: Get repository singleton
  - Lines 9-11: Initialize services with dependencies
- **Lines 14-16**: Root endpoint
  - Line 14: `@app.get("/")` - Health check endpoint
  - Line 16: Return simple status
- **Lines 19-31**: Supplier endpoints
  - Line 20: `@app.post("/suppliers")` - Create supplier
  - Line 21: Accept name, email, phone as query parameters (simple)
  - Line 22: Call service to create supplier
  - Line 23: Return response with ID and status
  - Line 26: `@app.get("/suppliers/{supplier_id}")` - Get supplier by ID
  - Lines 29-30: Raise 404 if not found
  - Line 31: Return supplier data
- **Lines 34-46**: Product endpoints
  - Line 35: `@app.post("/products")` - Create product
  - Line 36: Accept sku, name, quantity, price as parameters
  - Line 37: Call service to create product
  - Line 38: Return response with ID and SKU
  - Line 41: `@app.get("/products/{product_id}")` - Get product by ID
  - Lines 44-45: Raise 404 if not found
  - Line 46: Return product data with quantity
- **Lines 49-62**: Order endpoints
  - Line 50: `@app.post("/orders")` - Create order
  - Line 51: Accept customer_id and items list
  - Line 52: Convert dict list to OrderItem objects
  - Line 53: Call service to create order
  - Line 54: Return response with order details
  - Line 57: `@app.get("/orders/{order_id}")` - Get order by ID
  - Lines 60-61: Raise 404 if not found
  - Line 62: Return order data with status
- **Lines 65-68**: Order processing endpoint
  - Line 65: `@app.post("/orders/{order_id}/process")` - Process order
  - Line 67: Call service to process order
  - Line 68: Return updated status

**What's NOT included**:
- Pydantic request models - Using simple parameters for clarity
- Authentication - Not needed for MVP
- Pagination - Not needed for small datasets
- Complex query filters - Keep it simple
- Middleware - No CORS, logging, etc.
- Response models - Return dicts directly

---

### `tests/test_order_flow.py` (44 lines)

**Purpose**: End-to-end test

**Format**: Single test function with complete flow validation (lines 6-39)

**Why this test**:
- **Line 1**: `from src.infrastructure.db import Repository` - Import repository for data access
- **Line 2**: Import services - Business logic layer
- **Line 3**: Import OrderItem model - Domain model
- **Line 6**: `def test_order_flow()` - Main test function
- **Line 7**: `Repository(":memory:")` - In-memory SQLite for isolated testing
  - No file I/O, faster tests
  - Clean slate for each test run
- **Lines 8-10**: Initialize services with in-memory repository
- **Lines 12-15**: Step 1 - Create supplier
  - Line 13: Call supplier service with test data
  - Line 14: Assert ID was assigned by database
  - Line 15: Print success message
- **Lines 17-20**: Step 2 - Create product
  - Line 18: Create product with SKU, name, quantity, price
  - Line 19: Assert ID was assigned
  - Line 20: Print success message
- **Lines 22-27**: Step 3 - Create order
  - Line 23: Create OrderItem with product_id, SKU, quantity, price
  - Line 24: Call order service to create order
  - Line 25: Assert order ID was assigned
  - Line 26: Assert total is correct (10 items × $25 = $250)
  - Line 27: Print success message
- **Lines 29-32**: Step 4 - Verify stock deducted
  - Line 30: Get updated product from database
  - Line 31: Assert quantity is now 90 (100 - 10)
  - Line 32: Print success message
- **Lines 34-37**: Step 5 - Process order
  - Line 35: Call order service to process order
  - Line 36: Assert status changed to "processing"
  - Line 37: Print success message
- **Line 39**: Print overall success message
- **Lines 42-43**: Main block to run test directly

**What's NOT included**:
- Unit tests for each component - One end-to-end test validates integration
- Mock objects - Use real in-memory DB for authenticity
- pytest fixtures - Simple function for clarity
- Integration tests with external services - No external dependencies
- Test database cleanup - In-memory DB auto-cleans

---

## Comparison: Original vs MVP

| Aspect | Original System | MVP |
|--------|----------------|-----|
| Lines of Code | ~10,000 | ~300 |
| Layers | 7+ | 4 |
| Dependencies | 20+ | 3 |
| Database | PostgreSQL | SQLite |
| Caching | Redis | None |
| Messaging | RabbitMQ | None |
| ORM | SQLAlchemy | Direct SQL |
| Models | Pydantic + Value Objects | Dataclasses |
| Events | Event-driven | None |
| Features | Analytics, Simulation, Forecasting | Core CRUD only |
| Setup Time | Hours | Minutes |
| Debug Difficulty | High | Low |

---

## When to Add Complexity Back

### Add PostgreSQL When:
- Multiple users need concurrent access
- Data size exceeds SQLite limits (~140TB)
- Need advanced features (JSONB, full-text search)

### Add Redis When:
- API response times are slow
- Need to cache frequently accessed data
- Need rate limiting

### Add RabbitMQ When:
- Need async order processing
- Need to integrate with external systems
- Need job queues

### Add Event-Driven Architecture When:
- Multiple systems need to react to changes
- Need loose coupling between modules
- Need audit trails

### Add Analytics When:
- Need to track KPIs
- Need business insights
- Need forecasting

### Add Simulation When:
- Need to test "what-if" scenarios
- Need to model supply chain disruptions
- Need capacity planning

---

## Key Principle

**Build ONE working vertical slice → then expand**

Not:

**Build entire system → then try to make it work**

The MVP demonstrates the core flow:
1. Create supplier
2. Create product
3. Create order
4. Process order

Each step works end-to-end. Once this is solid, add complexity incrementally.

---

## Next Steps (After MVP Works)

1. **Add input validation** - Pydantic models for API requests
2. **Add authentication** - Simple API key or JWT
3. **Add error handling** - Custom exceptions, logging
4. **Add more endpoints** - List all, update, delete
5. **Add tests** - Unit tests for each service
6. **Add documentation** - API docs with examples
7. **Migrate to PostgreSQL** - When scale is needed
8. **Add caching** - When performance is needed
9. **Add analytics** - When insights are needed

---

## Conclusion

The MVP prioritizes:
- ✅ Working code over perfect architecture
- ✅ Simplicity over completeness
- ✅ Understanding over abstraction
- ✅ Speed of iteration over feature completeness

The original system is not "wrong" - it's just over-engineered for the current stage. The MVP provides a solid foundation that can evolve into the original architecture as needs arise.
