# Logistics MVP

A simplified, clean logistics management system.

## Features

- **Inventory Management**: Track items, stock levels, and reorder points
- **Supplier Management**: Manage suppliers and their information
- **Order Processing**: Create, process, and cancel orders with stock reservation

## Architecture

Simplified 3-layer architecture:
- **Models**: Pydantic models for data validation
- **Services**: Business logic layer
- **Repository**: Data access with SQLAlchemy
- **API**: FastAPI REST endpoints

## Setup

### Installation

```bash
cd mvp
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env` to set your database URL (default: SQLite)

## Running

### Start API Server

```bash
uvicorn src.api.main:app --reload
```

API will be available at `http://localhost:8000`

### API Documentation

Open `http://localhost:8000/docs` for interactive API documentation.

## Testing

```bash
pytest
```

## API Endpoints

### Suppliers
- `POST /api/v1/suppliers` - Create supplier
- `GET /api/v1/suppliers/{id}` - Get supplier
- `GET /api/v1/suppliers` - List suppliers

### Inventory
- `POST /api/v1/items` - Create item
- `GET /api/v1/items/{id}` - Get item
- `GET /api/v1/items` - List items
- `GET /api/v1/items/low-stock` - Get low stock items
- `PATCH /api/v1/items/{id}/stock` - Adjust stock

### Orders
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/{id}` - Get order
- `GET /api/v1/orders` - List orders
- `POST /api/v1/orders/{id}/process` - Process order
- `POST /api/v1/orders/{id}/cancel` - Cancel order

## Example Flow

```bash
# 1. Create a supplier
curl -X POST http://localhost:8000/api/v1/suppliers \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Supplies","email":"acme@example.com","phone":"555-0100","rating":4.5}'

# 2. Create an item
curl -X POST http://localhost:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"sku":"WIDGET-001","name":"Widget A","quantity":100,"unit_cost":25.00}'

# 3. Create an order
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST-001","items":[{"item_id":"<item_id>","sku":"WIDGET-001","quantity":10,"unit_price":25.00}]}'

# 4. Process the order
curl -X POST http://localhost:8000/api/v1/orders/<order_id>/process
```

## Development

This MVP intentionally keeps complexity low:
- No event-driven architecture
- No caching layer
- No message queues
- No external API integrations
- No advanced analytics

These can be added incrementally as needed.
