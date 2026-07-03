# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently using API key authentication (to be implemented).

## Endpoints

### Inventory

#### List Items
```http
GET /inventory/items
```

**Query Parameters:**
- `category` (optional): Filter by category
- `location` (optional): Filter by location

**Response:**
```json
{
  "items": [
    {
      "id": "item-001",
      "sku": "ITEM-001",
      "name": "Widget A",
      "quantity": 100
    }
  ],
  "total": 1
}
```

#### Create Item
```http
POST /inventory/items
```

**Request Body:**
```json
{
  "sku": "ITEM-001",
  "name": "Widget A",
  "quantity": 100,
  "unit_cost": 25.00,
  "location": "WH-A-01",
  "category": "widgets",
  "reorder_point": 20,
  "lead_time_days": 7
}
```

**Response:**
```json
{
  "id": "item-123",
  "sku": "ITEM-001",
  "status": "created"
}
```

#### Adjust Stock
```http
PATCH /inventory/items/{item_id}/stock
```

**Request Body:**
```json
{
  "quantity": 10,
  "reason": "Restock"
}
```

#### Get Low Stock Items
```http
GET /inventory/items/low-stock
```

### Orders

#### List Orders
```http
GET /orders/
```

**Query Parameters:**
- `customer_id` (optional): Filter by customer
- `status` (optional): Filter by status

#### Create Order
```http
POST /orders/
```

**Request Body:**
```json
{
  "customer_id": "cust-001",
  "items": [
    {
      "item_id": "item-001",
      "sku": "ITEM-001",
      "quantity": 10,
      "unit_price": 25.00
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Test City",
    "state": "TS",
    "postal_code": "12345",
    "country": "USA"
  },
  "billing_address": {
    "street": "123 Main St",
    "city": "Test City",
    "state": "TS",
    "postal_code": "12345",
    "country": "USA"
  }
}
```

#### Process Order
```http
POST /orders/{order_id}/process
```

#### Cancel Order
```http
POST /orders/{order_id}/cancel
```

### Suppliers

#### List Suppliers
```http
GET /suppliers/
```

#### Register Supplier
```http
POST /suppliers/
```

**Request Body:**
```json
{
  "name": "Acme Supplies",
  "contact_email": "contact@acme.com",
  "phone": "555-0100",
  "address": {
    "street": "123 Industrial Blvd",
    "city": "Chicago",
    "state": "IL",
    "postal_code": "60601",
    "country": "USA"
  },
  "payment_terms": "NET 30",
  "lead_time_days": 7
}
```

#### Evaluate Supplier
```http
GET /suppliers/{supplier_id}/score
```

### Shipments

#### Create Shipment
```http
POST /shipments/
```

#### Track Shipment
```http
GET /shipments/{shipment_id}/track
```

### Warehouses

#### List Warehouses
```http
GET /warehouses/
```

#### Get Utilization
```http
GET /warehouses/{warehouse_id}/utilization
```

### Analytics

#### Inventory Turnover
```http
GET /analytics/inventory/turnover
```

#### Supplier Performance
```http
GET /analytics/supplier/performance?supplier_id={supplier_id}
```

#### Risk Assessment
```http
GET /analytics/risk/assessment
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "type": "ErrorType",
  "details": {}
}
```

### Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error
