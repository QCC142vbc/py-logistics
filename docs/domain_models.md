# Domain Models Documentation

## Inventory

### Item
Represents a physical item in inventory.

**Attributes:**
- `id`: Unique identifier
- `sku`: Stock keeping unit
- `name`: Item name
- `quantity`: Current quantity
- `unit_cost`: Cost per unit
- `location`: Storage location
- `category`: Item category
- `reorder_point`: Minimum stock level
- `lead_time_days`: Supplier lead time

**Methods:**
- `is_below_reorder_point()`: Check if stock needs replenishment
- `total_value`: Calculate total inventory value

### StockLevel
Tracks stock availability across different states.

**Attributes:**
- `item_id`: Item identifier
- `available`: Available for sale
- `reserved`: Reserved for orders
- `in_transit`: In transit to warehouse
- `on_order`: On order from suppliers

**Methods:**
- `total_quantity`: Sum of all quantities
- `available_for_reservation`: Available for new reservations

## Supplier

### Supplier
Represents a supplier in the system.

**Attributes:**
- `id`: Unique identifier
- `name`: Supplier name
- `contact_email`: Email address
- `phone`: Phone number
- `address`: Physical address
- `rating`: Performance rating (0-5)
- `active`: Active status
- `payment_terms`: Payment terms
- `lead_time_days`: Standard lead time

**Methods:**
- `is_preferred`: Check if rating >= 4.0

### SupplierScore
Performance metrics for a supplier.

**Attributes:**
- `supplier_id`: Supplier identifier
- `reliability_score`: Delivery reliability (0-100)
- `quality_score`: Quality acceptance rate (0-100)
- `cost_score`: Cost competitiveness (0-100)
- `delivery_score`: On-time delivery (0-100)
- `overall_score`: Weighted average

**Methods:**
- `risk_level`: LOW, MEDIUM, HIGH, or CRITICAL

## Order

### Order
Represents a customer order.

**Attributes:**
- `id`: Unique identifier
- `customer_id`: Customer identifier
- `order_date`: Order creation date
- `status`: Order status (pending, confirmed, processing, shipped, delivered, cancelled)
- `items`: List of order items
- `total_amount`: Order total
- `shipping_address`: Delivery address
- `billing_address`: Billing address

**Methods:**
- `can_be_cancelled`: Check if order can be cancelled
- `is_complete`: Check if order is delivered

### OrderItem
Individual item within an order.

**Attributes:**
- `item_id`: Item identifier
- `sku`: Item SKU
- `quantity`: Quantity ordered
- `unit_price`: Price per unit

**Methods:**
- `subtotal`: Calculate line item total

## Transportation

### Shipment
Represents a shipment of goods.

**Attributes:**
- `id`: Unique identifier
- `order_id`: Associated order
- `route_id`: Planned route
- `carrier`: Shipping carrier
- `tracking_number`: Tracking number
- `status`: Shipment status
- `estimated_arrival`: Expected delivery date
- `items`: Shipment items

**Methods:**
- `is_delivered`: Check if shipment is delivered
- `is_in_transit`: Check if shipment is en route

### Route
Represents a transportation route.

**Attributes:**
- `id`: Unique identifier
- `origin`: Starting location
- `destination`: Ending location
- `transport_mode`: Transport mode (road, rail, air, sea)
- `distance_km`: Distance in kilometers
- `estimated_duration_hours`: Estimated travel time
- `cost`: Transportation cost

## Warehouse

### Warehouse
Represents a storage facility.

**Attributes:**
- `id`: Unique identifier
- `name`: Warehouse name
- `location`: Physical address
- `capacity_sqm`: Total capacity in square meters
- `utilized_sqm`: Currently utilized space
- `manager_id`: Manager identifier
- `operating_hours`: Operating hours
- `warehouse_type`: Type (distribution, fulfillment, cold_storage)

**Methods:**
- `utilization_percentage`: Calculate space utilization
- `is_at_capacity`: Check if full
- `is_near_capacity`: Check if approaching capacity

### StorageLocation
Specific storage location within a warehouse.

**Attributes:**
- `warehouse_id`: Warehouse identifier
- `zone`: Storage zone
- `aisle`: Aisle number
- `shelf`: Shelf number
- `bin`: Bin number
- `capacity_units`: Total capacity
- `current_units`: Current usage
- `item_type`: Type of items stored

**Methods:**
- `available_capacity`: Remaining capacity
- `utilization_percentage`: Space utilization
- `location_code`: Full location code
- `can_accommodate(quantity)`: Check if can store quantity
