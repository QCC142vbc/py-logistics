# Logistics Project Structure - Clean Architecture

```
logistics_project/
│
├── README.md                          # Project documentation, setup instructions
├── requirements.txt                   # Python dependencies with versions
├── pyproject.toml                     # Modern Python project configuration
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore patterns
├── docker-compose.yml                 # Container orchestration
├── Dockerfile                         # Application container definition
│
├── src/
│   ├── __init__.py
│   │
│   ├── domain/                        # Core business logic (no external dependencies)
│   │   ├── __init__.py
│   │   │
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Item(id: str, sku: str, name: str, quantity: int, unit_cost: Decimal, location: str, category: str, reorder_point: int, lead_time_days: int)
│   │   │   │                         # class StockLevel(item_id: str, available: int, reserved: int, in_transit: int, on_order: int, last_updated: datetime)
│   │   │   │                         # class InventoryTransaction(id: str, item_id: str, transaction_type: TransactionType, quantity: int, reference_id: str, timestamp: datetime)
│   │   │   │                         # enum TransactionType: RECEIPT, SHIPMENT, ADJUSTMENT, TRANSFER
│   │   │   │
│   │   │   ├── repository.py          # abstract class InventoryRepository(ABC)
│   │   │   │                         # async def get_item(item_id: str) -> Optional[Item]
│   │   │   │                         # async def get_item_by_sku(sku: str) -> Optional[Item]
│   │   │   │                         # async def save_item(item: Item) -> None
│   │   │   │                         # async def get_stock_level(item_id: str) -> Optional[StockLevel]
│   │   │   │                         # async def update_stock_level(item_id: str, delta: int) -> StockLevel
│   │   │   │                         # async def list_items(filter: ItemFilter) -> List[Item]
│   │   │   │                         # async def record_transaction(transaction: InventoryTransaction) -> None
│   │   │   │
│   │   │   ├── services.py           # class InventoryService(repository: InventoryRepository)
│   │   │   │                         # async def add_item(item: Item) -> Item
│   │   │   │                         # async def adjust_stock(item_id: str, quantity: int, reason: str) -> StockLevel
│   │   │   │                         # async def reserve_stock(item_id: str, quantity: int, order_id: str) -> bool
│   │   │   │                         # async def release_reservation(item_id: str, quantity: int, order_id: str) -> bool
│   │   │   │                         # async def check_availability(item_id: str, quantity: int) -> bool
│   │   │   │                         # async def get_low_stock_items(threshold: Optional[int] = None) -> List[Item]
│   │   │   │                         # async def transfer_stock(item_id: str, from_location: str, to_location: str, quantity: int) -> bool
│   │   │   │
│   │   │   ├── value_objects.py      # class SKU(value: str) - validation logic
│   │   │   │                         # class Quantity(value: int) - non-negative validation
│   │   │   │                         # class Location(value: str) - warehouse location format
│   │   │   │
│   │   │   └── exceptions.py         # class ItemNotFoundError(DomainException)
│   │   │                             # class InsufficientStockError(DomainException)
│   │   │                             # class InvalidSKUError(DomainException)
│   │   │
│   │   ├── supplier/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Supplier(id: str, name: str, contact_email: str, phone: str, address: Address, rating: float, active: bool, payment_terms: str, lead_time_days: int)
│   │   │   │                         # class SupplierScore(supplier_id: str, reliability_score: float, quality_score: float, cost_score: float, delivery_score: float, overall_score: float, last_calculated: datetime)
│   │   │   │                         # class SupplierContract(id: str, supplier_id: str, start_date: date, end_date: date, min_order_quantity: int, unit_price: Decimal, terms: str)
│   │   │   │                         # class Address(street: str, city: str, state: str, postal_code: str, country: str)
│   │   │   │
│   │   │   ├── repository.py          # abstract class SupplierRepository(ABC)
│   │   │   │                         # async def get_supplier(supplier_id: str) -> Optional[Supplier]
│   │   │   │                         # async def save_supplier(supplier: Supplier) -> None
│   │   │   │                         # async def list_suppliers(filter: SupplierFilter) -> List[Supplier]
│   │   │   │                         # async def get_active_suppliers() -> List[Supplier]
│   │   │   │                         # async def update_score(score: SupplierScore) -> None
│   │   │   │
│   │   │   ├── services.py           # class SupplierService(repository: SupplierRepository, score_calculator: ScoreCalculator)
│   │   │   │                         # async def register_supplier(supplier: Supplier) -> Supplier
│   │   │   │                         # async def update_supplier(supplier_id: str, updates: Dict[str, Any]) -> Supplier
│   │   │   │                         # async def evaluate_supplier(supplier_id: str) -> SupplierScore
│   │   │   │                         # async def get_best_suppliers_for_item(item_category: str, limit: int = 5) -> List[Supplier]
│   │   │   │                         # async def deactivate_supplier(supplier_id: str, reason: str) -> None
│   │   │   │
│   │   │   ├── scoring.py            # class ScoreCalculator
│   │   │   │                         # def calculate_reliability(delivery_history: List[DeliveryRecord]) -> float
│   │   │   │                         # def calculate_quality(quality_records: List[QualityRecord]) -> float
│   │   │   │                         # def calculate_cost(prices: List[Decimal], market_average: Decimal) -> float
│   │   │   │                         # def calculate_delivery(on_time_deliveries: int, total_deliveries: int) -> float
│   │   │   │
│   │   │   └── exceptions.py         # class SupplierNotFoundError(DomainException)
│   │   │                             # class DuplicateSupplierError(DomainException)
│   │   │
│   │   ├── order/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Order(id: str, customer_id: str, order_date: datetime, status: OrderStatus, items: List[OrderItem], total_amount: Decimal, shipping_address: Address, billing_address: Address)
│   │   │   │                         # class OrderItem(item_id: str, sku: str, quantity: int, unit_price: Decimal, subtotal: Decimal)
│   │   │   │                         # enum OrderStatus: PENDING, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED, RETURNED
│   │   │   │                         # class PurchaseOrder(id: str, supplier_id: str, order_date: datetime, status: PurchaseOrderStatus, items: List[PurchaseOrderItem], total_amount: Decimal, expected_delivery: date)
│   │   │   │                         # class PurchaseOrderItem(item_id: str, quantity: int, unit_price: Decimal, expected_delivery_date: date)
│   │   │   │                         # enum PurchaseOrderStatus: DRAFT, SENT, ACKNOWLEDGED, PARTIAL_RECEIVED, RECEIVED, CANCELLED
│   │   │   │
│   │   │   ├── repository.py          # abstract class OrderRepository(ABC)
│   │   │   │                         # async def get_order(order_id: str) -> Optional[Order]
│   │   │   │                         # async def save_order(order: Order) -> None
│   │   │   │                         # async def get_orders_by_customer(customer_id: str) -> List[Order]
│   │   │   │                         # async def get_orders_by_status(status: OrderStatus) -> List[Order]
│   │   │   │                         # async def get_purchase_order(po_id: str) -> Optional[PurchaseOrder]
│   │   │   │                         # async def save_purchase_order(po: PurchaseOrder) -> None
│   │   │   │
│   │   │   ├── services.py           # class OrderService(order_repo: OrderRepository, inventory_service: InventoryService)
│   │   │   │                         # async def create_order(order: Order) -> Order
│   │   │   │                         # async def confirm_order(order_id: str) -> Order
│   │   │   │                         # async def process_order(order_id: str) -> bool
│   │   │   │                         # async def cancel_order(order_id: str, reason: str) -> bool
│   │   │   │                         # async def update_order_status(order_id: str, status: OrderStatus) -> Order
│   │   │   │                         # async def create_purchase_order(po: PurchaseOrder) -> PurchaseOrder
│   │   │   │                         # async def receive_purchase_order(po_id: str, received_items: Dict[str, int]) -> PurchaseOrder
│   │   │   │
│   │   │   ├── validation.py         # class OrderValidator
│   │   │   │                         # def validate_order(order: Order) -> ValidationResult
│   │   │   │                         # def validate_items_availability(items: List[OrderItem], inventory: InventoryService) -> bool
│   │   │   │                         # def validate_payment_method(payment_info: PaymentInfo) -> bool
│   │   │   │
│   │   │   └── exceptions.py         # class OrderNotFoundError(DomainException)
│   │   │                             # class InvalidOrderStatusError(DomainException)
│   │   │                             # class OrderProcessingError(DomainException)
│   │   │
│   │   ├── transportation/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Route(id: str, origin: Location, destination: Location, distance_km: float, estimated_duration_hours: float, cost: Decimal, transport_mode: TransportMode)
│   │   │   │                         # class Shipment(id: str, order_id: str, route_id: str, carrier: str, tracking_number: str, status: ShipmentStatus, estimated_arrival: datetime, actual_arrival: Optional[datetime])
│   │   │   │                         # class ShipmentItem(shipment_id: str, item_id: str, quantity: int)
│   │   │   │                         # class Carrier(id: str, name: str, contact_email: str, phone: str, services: List[CarrierService], rating: float)
│   │   │   │                         # class CarrierService(service_type: str, base_rate: Decimal, rate_per_km: Decimal, max_weight_kg: float)
│   │   │   │                         # enum TransportMode: TRUCK, RAIL, AIR, SEA, MULTIMODAL
│   │   │   │                         # enum ShipmentStatus: PENDING, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, DELAYED, CANCELLED
│   │   │   │
│   │   │   ├── repository.py          # abstract class TransportationRepository(ABC)
│   │   │   │                         # async def get_shipment(shipment_id: str) -> Optional[Shipment]
│   │   │   │                         # async def save_shipment(shipment: Shipment) -> None
│   │   │   │                         # async def get_route(route_id: str) -> Optional[Route]
│   │   │   │                         # async def save_route(route: Route) -> None
│   │   │   │                         # async def get_carrier(carrier_id: str) -> Optional[Carrier]
│   │   │   │                         # async def list_carriers() -> List[Carrier]
│   │   │   │
│   │   │   ├── services.py           # class TransportationService(repo: TransportationRepository, routing_engine: RoutingEngine)
│   │   │   │                         # async def create_shipment(shipment: Shipment) -> Shipment
│   │   │   │                         # async def plan_route(origin: Location, destination: Location, constraints: RouteConstraints) -> Route
│   │   │   │                         # async def select_carrier(route: Route, requirements: ShipmentRequirements) -> Carrier
│   │   │   │                         # async def track_shipment(shipment_id: str) -> ShipmentStatus
│   │   │   │                         # async def update_shipment_status(shipment_id: str, status: ShipmentStatus) -> Shipment
│   │   │   │                         # async def calculate_shipping_cost(route: Route, weight_kg: float, volume_m3: float) -> Decimal
│   │   │   │
│   │   │   ├── routing.py            # class RoutingEngine
│   │   │   │                         # def find_shortest_path(origin: Location, destination: Location, graph: TransportGraph) -> Route
│   │   │   │                         # def find_cheapest_path(origin: Location, destination: Location, graph: TransportGraph) -> Route
│   │   │   │                         # def find_fastest_path(origin: Location, destination: Location, graph: TransportGraph) -> Route
│   │   │   │                         # def optimize_multi_stop(locations: List[Location], constraints: RouteConstraints) -> List[Route]
│   │   │   │
│   │   │   └── exceptions.py         # class ShipmentNotFoundError(DomainException)
│   │   │                             # class RouteNotFoundError(DomainException)
│   │   │                             # class CarrierUnavailableError(DomainException)
│   │   │
│   │   ├── warehouse/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Warehouse(id: str, name: str, location: Address, capacity_sqm: float, utilized_sqm: float, manager_id: str, operating_hours: OperatingHours)
│   │   │   │                         # class StorageLocation(warehouse_id: str, zone: str, aisle: str, shelf: str, bin: str, capacity_units: int, current_units: int, item_type: str)
│   │   │   │                         # class WarehouseTransfer(id: str, from_warehouse_id: str, to_warehouse_id: str, items: List[TransferItem], status: TransferStatus, initiated_by: str, initiated_at: datetime)
│   │   │   │                         # class TransferItem(item_id: str, quantity: int)
│   │   │   │                         # class OperatingHours(open_time: time, close_time: time, days_open: List[DayOfWeek])
│   │   │   │                         # enum TransferStatus: PENDING, APPROVED, IN_TRANSIT, RECEIVED, CANCELLED
│   │   │   │
│   │   │   ├── repository.py          # abstract class WarehouseRepository(ABC)
│   │   │   │                         # async def get_warehouse(warehouse_id: str) -> Optional[Warehouse]
│   │   │   │                         # async def save_warehouse(warehouse: Warehouse) -> None
│   │   │   │                         # async def list_warehouses() -> List[Warehouse]
│   │   │   │                         # async def get_storage_location(location_id: str) -> Optional[StorageLocation]
│   │   │   │                         # async def find_available_storage(warehouse_id: str, item_type: str, required_units: int) -> Optional[StorageLocation]
│   │   │   │                         # async def save_transfer(transfer: WarehouseTransfer) -> None
│   │   │   │
│   │   │   ├── services.py           # class WarehouseService(repo: WarehouseRepository, inventory_service: InventoryService)
│   │   │   │                         # async def register_warehouse(warehouse: Warehouse) -> Warehouse
│   │   │   │                         # async def allocate_storage(item_id: str, warehouse_id: str, quantity: int) -> StorageLocation
│   │   │   │                         # async def initiate_transfer(transfer: WarehouseTransfer) -> WarehouseTransfer
│   │   │   │                         # async def complete_transfer(transfer_id: str) -> WarehouseTransfer
│   │   │   │                         # async def get_warehouse_utilization(warehouse_id: str) -> float
│   │   │   │                         # async def optimize_storage_layout(warehouse_id: str) -> List[StorageRecommendation]
│   │   │   │
│   │   │   └── exceptions.py         # class WarehouseNotFoundError(DomainException)
│   │   │                             # class InsufficientCapacityError(DomainException)
│   │   │                             # class StorageLocationNotFoundError(DomainException)
│   │   │
│   │   ├── common/
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # class Entity(id: str, created_at: datetime, updated_at: datetime)
│   │   │   │                         # class Money(amount: Decimal, currency: str)
│   │   │   │                         # class Location(latitude: float, longitude: float, address: Optional[str])
│   │   │   │
│   │   │   ├── exceptions.py         # class DomainException(Exception)
│   │   │   │                         # class ValidationException(DomainException)
│   │   │   │                         # class NotFoundException(DomainException)
│   │   │   │                         # class BusinessRuleException(DomainException)
│   │   │   │
│   │   │   └── types.py              # type aliases: EntityId, Quantity, Amount, Timestamp
│   │   │
│   │   └── events/
│   │       ├── __init__.py
│   │       ├── models.py              # class DomainEvent(event_id: str, event_type: str, aggregate_id: str, data: Dict[str, Any], occurred_at: datetime, version: int)
│   │       │                         # class OrderCreatedEvent(DomainEvent)
│   │       │                         # class InventoryLowEvent(DomainEvent)
│   │       │                         # class ShipmentDeliveredEvent(DomainEvent)
│   │       │
│   │       ├── handlers.py           # class EventHandler(ABC)
│   │       │                         # async def handle(event: DomainEvent) -> None
│   │       │
│   │       └── dispatcher.py         # class EventDispatcher
│   │                                   # async def publish(event: DomainEvent) -> None
│   │                                   # def subscribe(event_type: str, handler: EventHandler) -> None
│   │
│   ├── application/                  # Use cases and application services
│   │   ├── __init__.py
│   │   │
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── inventory/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_item.py     # class CreateItemUseCase(inventory_service: InventoryService)
│   │   │   │   │                     # async def execute(request: CreateItemRequest) -> CreateItemResponse
│   │   │   │   │                     # class CreateItemRequest(sku: str, name: str, quantity: int, unit_cost: Decimal, location: str, category: str, reorder_point: int, lead_time_days: int)
│   │   │   │   │                     # class CreateItemResponse(item_id: str, sku: str, status: str)
│   │   │   │   │
│   │   │   │   ├── adjust_stock.py    # class AdjustStockUseCase(inventory_service: InventoryService)
│   │   │   │   │                     # async def execute(request: AdjustStockRequest) -> AdjustStockResponse
│   │   │   │   │                     # class AdjustStockRequest(item_id: str, quantity: int, reason: str)
│   │   │   │   │                     # class AdjustStockResponse(item_id: str, new_quantity: int, transaction_id: str)
│   │   │   │   │
│   │   │   │   ├── reserve_stock.py   # class ReserveStockUseCase(inventory_service: InventoryService)
│   │   │   │   │                     # async def execute(request: ReserveStockRequest) -> ReserveStockResponse
│   │   │   │   │                     # class ReserveStockRequest(item_id: str, quantity: int, order_id: str)
│   │   │   │   │                     # class ReserveStockResponse(success: bool, reserved_quantity: int)
│   │   │   │   │
│   │   │   │   └── get_inventory.py   # class GetInventoryUseCase(inventory_service: InventoryService)
│   │   │   │                         # async def execute(request: GetInventoryRequest) -> GetInventoryResponse
│   │   │   │                         # class GetInventoryRequest(filter: Optional[InventoryFilter] = None)
│   │   │   │                         # class GetInventoryResponse(items: List[ItemDTO], total: int)
│   │   │   │
│   │   │   ├── order/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_order.py     # class CreateOrderUseCase(order_service: OrderService, inventory_service: InventoryService)
│   │   │   │   │                     # async def execute(request: CreateOrderRequest) -> CreateOrderResponse
│   │   │   │   │                     # class CreateOrderRequest(customer_id: str, items: List[OrderItemRequest], shipping_address: AddressDTO, billing_address: AddressDTO)
│   │   │   │   │                     # class CreateOrderResponse(order_id: str, status: OrderStatus, total_amount: Decimal)
│   │   │   │   │
│   │   │   │   ├── process_order.py    # class ProcessOrderUseCase(order_service: OrderService, inventory_service: InventoryService, transportation_service: TransportationService)
│   │   │   │   │                     # async def execute(request: ProcessOrderRequest) -> ProcessOrderResponse
│   │   │   │   │                     # class ProcessOrderRequest(order_id: str)
│   │   │   │   │                     # class ProcessOrderResponse(success: bool, shipment_id: Optional[str])
│   │   │   │   │
│   │   │   │   ├── cancel_order.py     # class CancelOrderUseCase(order_service: OrderService)
│   │   │   │   │                     # async def execute(request: CancelOrderRequest) -> CancelOrderResponse
│   │   │   │   │                     # class CancelOrderRequest(order_id: str, reason: str)
│   │   │   │   │                     # class CancelOrderResponse(success: bool, refund_amount: Optional[Decimal])
│   │   │   │   │
│   │   │   │   └── get_order.py        # class GetOrderUseCase(order_service: OrderService)
│   │   │   │                         # async def execute(request: GetOrderRequest) -> GetOrderResponse
│   │   │   │                         # class GetOrderRequest(order_id: str)
│   │   │   │                         # class GetOrderResponse(order: OrderDTO)
│   │   │   │
│   │   │   ├── supplier/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── register_supplier.py # class RegisterSupplierUseCase(supplier_service: SupplierService)
│   │   │   │   │                     # async def execute(request: RegisterSupplierRequest) -> RegisterSupplierResponse
│   │   │   │   │                     # class RegisterSupplierRequest(name: str, contact_email: str, phone: str, address: AddressDTO, payment_terms: str, lead_time_days: int)
│   │   │   │   │                     # class RegisterSupplierResponse(supplier_id: str, status: str)
│   │   │   │   │
│   │   │   │   ├── evaluate_supplier.py # class EvaluateSupplierUseCase(supplier_service: SupplierService)
│   │   │   │   │                     # async def execute(request: EvaluateSupplierRequest) -> EvaluateSupplierResponse
│   │   │   │   │                     # class EvaluateSupplierRequest(supplier_id: str)
│   │   │   │   │                     # class EvaluateSupplierResponse(supplier_id: str, scores: SupplierScoreDTO)
│   │   │   │   │
│   │   │   │   └── create_purchase_order.py # class CreatePurchaseOrderUseCase(order_service: OrderService, supplier_service: SupplierService)
│   │   │   │                         # async def execute(request: CreatePurchaseOrderRequest) -> CreatePurchaseOrderResponse
│   │   │   │                         # class CreatePurchaseOrderRequest(supplier_id: str, items: List[PurchaseOrderItemRequest])
│   │   │   │                         # class CreatePurchaseOrderResponse(po_id: str, status: PurchaseOrderStatus)
│   │   │   │
│   │   │   ├── transportation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_shipment.py  # class CreateShipmentUseCase(transportation_service: TransportationService)
│   │   │   │   │                     # async def execute(request: CreateShipmentRequest) -> CreateShipmentResponse
│   │   │   │   │                     # class CreateShipmentRequest(order_id: str, origin: LocationDTO, destination: LocationDTO, items: List[ShipmentItemRequest], requirements: ShipmentRequirementsDTO)
│   │   │   │   │                     # class CreateShipmentResponse(shipment_id: str, tracking_number: str, estimated_arrival: datetime)
│   │   │   │   │
│   │   │   │   ├── track_shipment.py   # class TrackShipmentUseCase(transportation_service: TransportationService)
│   │   │   │   │                     # async def execute(request: TrackShipmentRequest) -> TrackShipmentResponse
│   │   │   │   │                     # class TrackShipmentRequest(shipment_id: str)
│   │   │   │   │                     # class TrackShipmentResponse(shipment_id: str, status: ShipmentStatus, current_location: Optional[LocationDTO], estimated_arrival: datetime)
│   │   │   │   │
│   │   │   │   └── plan_route.py       # class PlanRouteUseCase(transportation_service: TransportationService)
│   │   │   │                         # async def execute(request: PlanRouteRequest) -> PlanRouteResponse
│   │   │   │                         # class PlanRouteRequest(origin: LocationDTO, destination: LocationDTO, constraints: RouteConstraintsDTO)
│   │   │   │                         # class PlanRouteResponse(route_id: str, distance_km: float, estimated_duration_hours: float, cost: Decimal, steps: List[RouteStepDTO])
│   │   │   │
│   │   │   └── warehouse/
│   │   │       ├── __init__.py
│   │   │       ├── register_warehouse.py # class RegisterWarehouseUseCase(warehouse_service: WarehouseService)
│   │   │       │                     # async def execute(request: RegisterWarehouseRequest) -> RegisterWarehouseResponse
│   │   │       │                     # class RegisterWarehouseRequest(name: str, location: AddressDTO, capacity_sqm: float, manager_id: str, operating_hours: OperatingHoursDTO)
│   │   │       │                     # class RegisterWarehouseResponse(warehouse_id: str, status: str)
│   │   │       │
│   │   │       ├── initiate_transfer.py # class InitiateTransferUseCase(warehouse_service: WarehouseService)
│   │   │       │                     # async def execute(request: InitiateTransferRequest) -> InitiateTransferResponse
│   │   │       │                     # class InitiateTransferRequest(from_warehouse_id: str, to_warehouse_id: str, items: List[TransferItemRequest], initiated_by: str)
│   │   │       │                     # class InitiateTransferResponse(transfer_id: str, status: TransferStatus)
│   │   │       │
│   │   │       └── get_utilization.py  # class GetUtilizationUseCase(warehouse_service: WarehouseService)
│   │   │                           # async def execute(request: GetUtilizationRequest) -> GetUtilizationResponse
│   │   │                           # class GetUtilizationRequest(warehouse_id: str)
│   │   │                           # class GetUtilizationResponse(warehouse_id: str, utilization_percentage: float, available_capacity_sqm: float)
│   │   │
│   │   ├── dto/
│   │   │   ├── __init__.py
│   │   │   ├── inventory.py          # class ItemDTO(id: str, sku: str, name: str, quantity: int, unit_cost: str, location: str, category: str)
│   │   │   │                         # class StockLevelDTO(item_id: str, available: int, reserved: int, in_transit: int)
│   │   │   │
│   │   │   ├── order.py              # class OrderDTO(id: str, customer_id: str, order_date: str, status: str, items: List[OrderItemDTO], total_amount: str)
│   │   │   │                         # class OrderItemDTO(item_id: str, sku: str, quantity: int, unit_price: str, subtotal: str)
│   │   │   │
│   │   │   ├── supplier.py          # class SupplierDTO(id: str, name: str, contact_email: str, rating: float, active: bool)
│   │   │   │                         # class SupplierScoreDTO(supplier_id: str, reliability_score: float, quality_score: float, cost_score: float, overall_score: float)
│   │   │   │
│   │   │   ├── transportation.py     # class ShipmentDTO(id: str, order_id: str, tracking_number: str, status: str, estimated_arrival: str)
│   │   │   │                         # class RouteDTO(id: str, origin: LocationDTO, destination: LocationDTO, distance_km: float, cost: str)
│   │   │   │
│   │   │   └── common.py             # class AddressDTO(street: str, city: str, state: str, postal_code: str, country: str)
│   │   │                         # class LocationDTO(latitude: float, longitude: float, address: Optional[AddressDTO])
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── notification_service.py # class NotificationService(email_client: EmailClient, sms_client: SMSClient)
│   │   │   │                         # async def send_order_confirmation(order_id: str, customer_email: str) -> None
│   │   │   │                         # async def send_shipment_update(shipment_id: str, recipient: str) -> None
│   │   │   │                         # async def send_low_stock_alert(item_id: str, recipients: List[str]) -> None
│   │   │   │
│   │   │   ├── reporting_service.py  # class ReportingService(analytics_engine: AnalyticsEngine)
│   │   │   │                         # async def generate_inventory_report(filter: ReportFilter) -> Report
│   │   │   │                         # async def generate_order_report(filter: ReportFilter) -> Report
│   │   │   │                         # async def generate_supplier_performance_report(supplier_id: str, date_range: DateRange) -> Report
│   │   │   │
│   │   │   └── audit_service.py     # class AuditService(audit_repository: AuditRepository)
│   │   │                           # async def log_action(action: AuditAction) -> None
│   │   │                           # async def get_audit_log(filter: AuditFilter) -> List[AuditEntry]
│   │   │
│   │   └── workflows/
│   │       ├── __init__.py
│   │       ├── order_fulfillment.py  # class OrderFulfillmentWorkflow(create_order: CreateOrderUseCase, process_order: ProcessOrderUseCase, create_shipment: CreateShipmentUseCase)
│   │       │                         # async def execute(request: OrderFulfillmentRequest) -> OrderFulfillmentResponse
│   │       │                         # class OrderFulfillmentRequest(customer_id: str, items: List[OrderItemRequest], shipping_address: AddressDTO)
│   │       │                         # class OrderFulfillmentResponse(order_id: str, shipment_id: str, estimated_delivery: datetime)
│   │       │
│   │       ├── replenishment.py      # class ReplenishmentWorkflow(inventory_service: InventoryService, supplier_service: SupplierService, create_purchase_order: CreatePurchaseOrderUseCase)
│   │       │                         # async def execute(request: ReplenishmentRequest) -> ReplenishmentResponse
│   │       │                         # class ReplenishmentRequest(item_id: str, quantity: int, preferred_supplier_id: Optional[str])
│   │       │                         # class ReplenishmentResponse(po_id: str, expected_delivery: date)
│   │       │
│   │       └── warehouse_transfer.py # class WarehouseTransferWorkflow(warehouse_service: WarehouseService, transportation_service: TransportationService)
│   │                               # async def execute(request: WarehouseTransferRequest) -> WarehouseTransferResponse
│   │                               # class WarehouseTransferRequest(from_warehouse_id: str, to_warehouse_id: str, items: List[TransferItemRequest])
│   │                               # class WarehouseTransferResponse(transfer_id: str, shipment_id: str, estimated_arrival: datetime)
│   │
│   ├── infrastructure/               # External dependencies implementation
│   │   ├── __init__.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py         # class DatabaseConnection(config: DatabaseConfig)
│   │   │   │                         # async def get_session() -> AsyncSession
│   │   │   │                         # async def close() -> None
│   │   │   │
│   │   │   ├── models.py             # SQLAlchemy ORM models
│   │   │   │                         # class ItemModel(Base): __tablename__ = "items"
│   │   │   │                         # class OrderModel(Base): __tablename__ = "orders"
│   │   │   │                         # class SupplierModel(Base): __tablename__ = "suppliers"
│   │   │   │                         # class ShipmentModel(Base): __tablename__ = "shipments"
│   │   │   │                         # class WarehouseModel(Base): __tablename__ = "warehouses"
│   │   │   │
│   │   │   ├── repositories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sql_inventory_repository.py # class SQLInventoryRepository(InventoryRepository, session_factory: SessionFactory)
│   │   │   │   │                     # async def get_item(item_id: str) -> Optional[Item]
│   │   │   │   │                     # async def save_item(item: Item) -> None
│   │   │   │   │                     # async def get_stock_level(item_id: str) -> Optional[StockLevel]
│   │   │   │   │                     # async def update_stock_level(item_id: str, delta: int) -> StockLevel
│   │   │   │   │
│   │   │   │   ├── sql_order_repository.py # class SQLOrderRepository(OrderRepository, session_factory: SessionFactory)
│   │   │   │   │                     # async def get_order(order_id: str) -> Optional[Order]
│   │   │   │   │                     # async def save_order(order: Order) -> None
│   │   │   │   │
│   │   │   │   ├── sql_supplier_repository.py # class SQLSupplierRepository(SupplierRepository, session_factory: SessionFactory)
│   │   │   │   │                     # async def get_supplier(supplier_id: str) -> Optional[Supplier]
│   │   │   │   │                     # async def save_supplier(supplier: Supplier) -> None
│   │   │   │   │
│   │   │   │   ├── sql_transportation_repository.py # class SQLTransportationRepository(TransportationRepository, session_factory: SessionFactory)
│   │   │   │   │                     # async def get_shipment(shipment_id: str) -> Optional[Shipment]
│   │   │   │   │                     # async def save_shipment(shipment: Shipment) -> None
│   │   │   │   │
│   │   │   │   └── sql_warehouse_repository.py # class SQLWarehouseRepository(WarehouseRepository, session_factory: SessionFactory)
│   │   │   │                         # async def get_warehouse(warehouse_id: str) -> Optional[Warehouse]
│   │   │   │                         # async def save_warehouse(warehouse: Warehouse) -> None
│   │   │   │
│   │   │   ├── migrations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── env.py            # Alembic environment configuration
│   │   │   │   └── versions/
│   │   │   │       ├── 001_initial.py # Initial schema creation
│   │   │   │       ├── 002_add_indexes.py # Add performance indexes
│   │   │   │       └── 003_add_audit_tables.py # Add audit logging tables
│   │   │   │
│   │   │   └── seed_data.py         # async def seed_items() -> None
│   │   │                             # async def seed_suppliers() -> None
│   │   │                             # async def seed_warehouses() -> None
│   │   │                             # async def seed_all() -> None
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── clients/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── carrier_api.py     # class CarrierAPIClient(base_url: str, api_key: str)
│   │   │   │   │                     # async def get_rates(origin: Location, destination: Location, weight: float) -> List[ShippingRate]
│   │   │   │   │                     # async def create_shipment(shipment_request: ShipmentRequest) -> ShipmentConfirmation
│   │   │   │   │                     # async def track_shipment(tracking_number: str) -> TrackingInfo
│   │   │   │   │
│   │   │   │   ├── payment_gateway.py # class PaymentGatewayAPIClient(api_key: str, secret: str)
│   │   │   │   │                     # async def process_payment(payment_request: PaymentRequest) -> PaymentResponse
│   │   │   │   │                     # async def refund_payment(transaction_id: str, amount: Decimal) -> RefundResponse
│   │   │   │   │
│   │   │   │   └── geocoding.py      # class GeocodingAPIClient(api_key: str)
│   │   │   │                         # async def geocode(address: str) -> Location
│   │   │   │                         # async def reverse_geocode(latitude: float, longitude: float) -> Address
│   │   │   │
│   │   │   └── webhooks/
│   │   │       ├── __init__.py
│   │   │       ├── carrier_webhook.py # async def handle_carrier_webhook(payload: Dict[str, Any]) -> WebhookResponse
│   │   │       └── payment_webhook.py # async def handle_payment_webhook(payload: Dict[str, Any]) -> WebhookResponse
│   │   │
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── redis_client.py       # class RedisClient(host: str, port: int, db: int)
│   │   │   │                         # async def get(key: str) -> Optional[str]
│   │   │   │                         # async def set(key: str, value: str, ttl: Optional[int] = None) -> None
│   │   │   │                         # async def delete(key: str) -> None
│   │   │   │                         # async def exists(key: str) -> bool
│   │   │   │
│   │   │   └── cache_service.py      # class CacheService(redis_client: RedisClient)
│   │   │                           # async def get_item(item_id: str) -> Optional[Item]
│   │   │                           # async def set_item(item_id: str, item: Item, ttl: int = 3600) -> None
│   │   │                           # async def invalidate_pattern(pattern: str) -> None
│   │   │
│   │   ├── messaging/
│   │   │   ├── __init__.py
│   │   │   ├── rabbitmq_publisher.py # class RabbitMQPublisher(host: str, queue: str)
│   │   │   │                         # async def publish(message: Dict[str, Any]) -> None
│   │   │   │                         # async def close() -> None
│   │   │   │
│   │   │   └── rabbitmq_consumer.py # class RabbitMQConsumer(host: str, queue: str)
│   │   │                           # async def consume(handler: Callable[[Dict[str, Any]], Awaitable[None]]) -> None
│   │   │                           # async def close() -> None
│   │   │
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── s3_client.py          # class S3Client(bucket_name: str, access_key: str, secret_key: str)
│   │   │   │                         # async def upload_file(key: str, content: bytes, content_type: str) -> str
│   │   │   │                         # async def download_file(key: str) -> bytes
│   │   │   │                         # async def delete_file(key: str) -> None
│   │   │   │                         # async def generate_presigned_url(key: str, expiration: int = 3600) -> str
│   │   │   │
│   │   │   └── document_storage.py  # class DocumentStorage(s3_client: S3Client)
│   │   │                           # async def save_invoice(order_id: str, invoice_pdf: bytes) -> str
│   │   │                           # async def get_invoice(order_id: str) -> bytes
│   │   │
│   │   └── logging/
│   │       ├── __init__.py
│   │       ├── logger.py             # class StructuredLogger(name: str, config: LoggingConfig)
│   │       │                         # def info(message: str, **kwargs) -> None
│   │       │                         # def error(message: str, **kwargs) -> None
│   │       │                         # def warning(message: str, **kwargs) -> None
│   │       │                         # def debug(message: str, **kwargs) -> None
│   │       │
│   │       └── middleware.py         # class LoggingMiddleware
│   │                                   # async def log_request(request: Request) -> None
│   │                                   # async def log_response(response: Response) -> None
│   │
│   ├── interfaces/                   # External interfaces (CLI, API, etc.)
│   │   ├── __init__.py
│   │   │
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # def main() -> None
│   │   │   │                         # async def cli() -> None
│   │   │   │
│   │   │   ├── commands/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── inventory.py      # def add_item(args: Namespace) -> None
│   │   │   │   │                     # def list_items(args: Namespace) -> None
│   │   │   │   │                     # def adjust_stock(args: Namespace) -> None
│   │   │   │   │
│   │   │   │   ├── order.py          # def create_order(args: Namespace) -> None
│   │   │   │   │                     # def list_orders(args: Namespace) -> None
│   │   │   │   │                     # def get_order(args: Namespace) -> None
│   │   │   │   │
│   │   │   │   ├── supplier.py       # def add_supplier(args: Namespace) -> None
│   │   │   │   │                     # def list_suppliers(args: Namespace) -> None
│   │   │   │   │                     # def evaluate_supplier(args: Namespace) -> None
│   │   │   │   │
│   │   │   │   └── shipment.py       # def track_shipment(args: Namespace) -> None
│   │   │   │                         # def create_shipment(args: Namespace) -> None
│   │   │   │
│   │   │   └── utils.py              # def print_table(data: List[Dict[str, Any]], columns: List[str]) -> None
│   │   │                           # def confirm_action(message: str) -> bool
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # async def create_app() -> FastAPI
│   │   │   │                         # def get_application() -> FastAPI
│   │   │   │
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── inventory.py      # router = APIRouter(prefix="/api/v1/inventory")
│   │   │   │   │                     # @router.post("/items", response_model=ItemDTO)
│   │   │   │   │                     # async def create_item(request: CreateItemRequest, use_case: CreateItemUseCase) -> ItemDTO
│   │   │   │   │                     # @router.get("/items", response_model=List[ItemDTO])
│   │   │   │   │                     # async def list_items(use_case: GetInventoryUseCase) -> List[ItemDTO]
│   │   │   │   │                     # @router.patch("/items/{item_id}/stock")
│   │   │   │   │                     # async def adjust_stock(item_id: str, request: AdjustStockRequest, use_case: AdjustStockUseCase) -> AdjustStockResponse
│   │   │   │   │
│   │   │   │   ├── orders.py         # router = APIRouter(prefix="/api/v1/orders")
│   │   │   │   │                     # @router.post("/", response_model=OrderDTO)
│   │   │   │   │                     # async def create_order(request: CreateOrderRequest, use_case: CreateOrderUseCase) -> OrderDTO
│   │   │   │   │                     # @router.get("/{order_id}", response_model=OrderDTO)
│   │   │   │   │                     # async def get_order(order_id: str, use_case: GetOrderUseCase) -> OrderDTO
│   │   │   │   │                     # @router.post("/{order_id}/process")
│   │   │   │   │                     # async def process_order(order_id: str, use_case: ProcessOrderUseCase) -> ProcessOrderResponse
│   │   │   │   │                     # @router.post("/{order_id}/cancel")
│   │   │   │   │                     # async def cancel_order(order_id: str, request: CancelOrderRequest, use_case: CancelOrderUseCase) -> CancelOrderResponse
│   │   │   │   │
│   │   │   │   ├── suppliers.py      # router = APIRouter(prefix="/api/v1/suppliers")
│   │   │   │   │                     # @router.post("/", response_model=SupplierDTO)
│   │   │   │   │                     # async def register_supplier(request: RegisterSupplierRequest, use_case: RegisterSupplierUseCase) -> SupplierDTO
│   │   │   │   │                     # @router.get("/", response_model=List[SupplierDTO])
│   │   │   │   │                     # async def list_suppliers() -> List[SupplierDTO]
│   │   │   │   │                     # @router.get("/{supplier_id}/score", response_model=SupplierScoreDTO)
│   │   │   │   │                     # async def evaluate_supplier(supplier_id: str, use_case: EvaluateSupplierUseCase) -> SupplierScoreDTO
│   │   │   │   │
│   │   │   │   ├── shipments.py      # router = APIRouter(prefix="/api/v1/shipments")
│   │   │   │   │                     # @router.post("/", response_model=ShipmentDTO)
│   │   │   │   │                     # async def create_shipment(request: CreateShipmentRequest, use_case: CreateShipmentUseCase) -> ShipmentDTO
│   │   │   │   │                     # @router.get("/{shipment_id}/track", response_model=TrackShipmentResponse)
│   │   │   │   │                     # async def track_shipment(shipment_id: str, use_case: TrackShipmentUseCase) -> TrackShipmentResponse
│   │   │   │   │
│   │   │   │   ├── warehouses.py     # router = APIRouter(prefix="/api/v1/warehouses")
│   │   │   │   │                     # @router.post("/", response_model=WarehouseDTO)
│   │   │   │   │                     # async def register_warehouse(request: RegisterWarehouseRequest, use_case: RegisterWarehouseUseCase) -> WarehouseDTO
│   │   │   │   │                     # @router.get("/", response_model=List[WarehouseDTO])
│   │   │   │   │                     # async def list_warehouses() -> List[WarehouseDTO]
│   │   │   │   │                     # @router.get("/{warehouse_id}/utilization")
│   │   │   │   │                     # async def get_utilization(warehouse_id: str, use_case: GetUtilizationUseCase) -> GetUtilizationResponse
│   │   │   │   │
│   │   │   │   └── analytics.py      # router = APIRouter(prefix="/api/v1/analytics")
│   │   │   │                         # @router.get("/inventory/turnover")
│   │   │   │                         # async def get_inventory_turnover(date_range: DateRange, analytics: AnalyticsEngine) -> Dict[str, float]
│   │   │   │                         # @router.get("/supplier/performance")
│   │   │   │                         # async def get_supplier_performance(supplier_id: str, analytics: AnalyticsEngine) -> SupplierPerformanceReport
│   │   │   │                         # @router.get("/risk/assessment")
│   │   │   │                         # async def get_risk_assessment(analytics: AnalyticsEngine) -> RiskAssessmentReport
│   │   │   │
│   │   │   ├── middleware/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # class AuthMiddleware
│   │   │   │   │                     # async def process_request(request: Request, call_next: Callable) -> Response
│   │   │   │   │
│   │   │   │   ├── error_handler.py  # async def handle_domain_exception(request: Request, exc: DomainException) -> JSONResponse
│   │   │   │   │                     # async def handle_validation_exception(request: Request, exc: ValidationException) -> JSONResponse
│   │   │   │   │
│   │   │   │   ├── cors.py           # class CORSMiddleware
│   │   │   │   │
│   │   │   │   └── rate_limit.py     # class RateLimitMiddleware
│   │   │   │                         # async def check_rate_limit(request: Request) -> bool
│   │   │   │
│   │   │   ├── dependencies/
│   │   │   │   ├── __init__.py
│   │   │   │   └── common.py         # async def get_inventory_service() -> InventoryService
│   │   │   │                         # async def get_order_service() -> OrderService
│   │   │   │                         # async def get_db_session() -> AsyncSession
│   │   │   │
│   │   │   └── schemas/
│   │   │       ├── __init__.py
│   │   │       ├── inventory.py      # Pydantic models for request/response validation
│   │   │       ├── orders.py
│   │   │       ├── suppliers.py
│   │   │       └── common.py
│   │   │
│   │   └── grpc/                     # Optional gRPC interface
│   │       ├── __init__.py
│   │       ├── server.py             # async def serve() -> None
│   │       └── services/
│   │           ├── __init__.py
│   │           ├── inventory_pb2.py  # Generated protobuf files
│   │           ├── inventory_pb2_grpc.py
│   │           └── inventory_service.py # class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer)
│   │
│   ├── analytics/                    # Advanced analytics and reporting
│   │   ├── __init__.py
│   │   │
│   │   ├── risk_scoring.py           # class RiskScoringEngine
│   │   │   │                         # def calculate_supplier_risk(supplier: Supplier, historical_data: SupplierHistory) -> RiskScore
│   │   │   │                         # def calculate_inventory_risk(item: Item, demand_history: DemandHistory) -> RiskScore
│   │   │   │                         # def calculate_supply_chain_risk(network: SupplyChainNetwork) -> SupplyChainRiskReport
│   │   │   │                         # class RiskScore(score: float, level: RiskLevel, factors: List[RiskFactor])
│   │   │   │                         # enum RiskLevel: LOW, MEDIUM, HIGH, CRITICAL
│   │   │   │                         # class RiskFactor(category: str, description: str, impact: float)
│   │   │   │
│   │   ├── optimization/
│   │   │   ├── __init__.py
│   │   │   ├── routing_optimizer.py # class RoutingOptimizer
│   │   │   │                         # def optimize_vehicle_route(depot: Location, deliveries: List[Delivery], constraints: RoutingConstraints) -> OptimizedRoute
│   │   │   │                         # def optimize_multi_depot(depots: List[Location], deliveries: List[Delivery]) -> MultiDepotSolution
│   │   │   │                         # class OptimizedRoute(route: List[Location], total_distance: float, total_time: float, cost: Decimal)
│   │   │   │
│   │   │   ├── inventory_optimizer.py # class InventoryOptimizer
│   │   │   │                         # def calculate_eoq(demand_rate: float, ordering_cost: Decimal, holding_cost: Decimal) -> EconomicOrderQuantity
│   │   │   │                         # def calculate_safety_stock(demand_std_dev: float, lead_time_std_dev: float, service_level: float) -> SafetyStockLevel
│   │   │   │                         # def optimize_reorder_points(items: List[Item]) -> List[ReorderPointRecommendation]
│   │   │   │                         # class EconomicOrderQuantity(quantity: int, order_frequency: float, total_cost: Decimal)
│   │   │   │
│   │   │   └── cost_optimizer.py     # class CostOptimizer
│   │   │                           # def minimize_transportation_cost(shipments: List[Shipment], carriers: List[Carrier]) -> CostOptimizationResult
│   │   │                           # def optimize_warehouse_allocation(orders: List[Order], warehouses: List[Warehouse]) -> AllocationResult
│   │   │                           # class CostOptimizationResult(total_cost: Decimal, savings: Decimal, recommendations: List[CostRecommendation])
│   │   │
│   │   ├── reporting/
│   │   │   ├── __init__.py
│   │   │   ├── report_generator.py  # class ReportGenerator
│   │   │   │                         # def generate_inventory_report(filter: ReportFilter, format: ReportFormat) -> Report
│   │   │   │                         # def generate_order_performance_report(date_range: DateRange) -> OrderPerformanceReport
│   │   │   │                         # def generate_supplier_scorecard(supplier_id: str, period: DateRange) -> SupplierScorecard
│   │   │   │                         # def generate_dashboard_metrics(date_range: DateRange) -> DashboardMetrics
│   │   │   │                         # enum ReportFormat: PDF, EXCEL, CSV, HTML
│   │   │   │
│   │   │   └── templates/
│   │   │       ├── inventory_report.html
│   │   │       ├── supplier_scorecard.html
│   │   │       └── dashboard.html
│   │   │
│   │   ├── forecasting/
│   │   │   ├── __init__.py
│   │   │   ├── demand_forecaster.py  # class DemandForecaster
│   │   │   │                         # def forecast_demand(item_id: str, horizon_days: int, method: ForecastMethod) -> DemandForecast
│   │   │   │                         # def forecast_seasonal_demand(item_id: str, periods: int) -> SeasonalForecast
│   │   │   │                         # class DemandForecast(item_id: str, forecast: List[DemandPoint], confidence_interval: List[Tuple[float, float]])
│   │   │   │                         # enum ForecastMethod: MOVING_AVERAGE, EXPONENTIAL_SMOOTHING, ARIMA, PROPHET, MACHINE_LEARNING
│   │   │   │
│   │   │   └── lead_time_forecaster.py # class LeadTimeForecaster
│   │   │                           # def forecast_lead_time(supplier_id: str, item_category: str) -> LeadTimeForecast
│   │   │                           # class LeadTimeForecast(supplier_id: str, expected_days: int, confidence: float, distribution: LeadTimeDistribution)
│   │   │
│   │   └── metrics/
│   │       ├── __init__.py
│   │       ├── kpi_calculator.py     # class KPICalculator
│   │       │                         # def calculate_inventory_turnover(cost_of_goods_sold: Decimal, average_inventory: Decimal) -> float
│   │       │                         # def calculate_order_fulfillment_rate(total_orders: int, fulfilled_orders: int) -> float
│   │       │                         # def calculate_on_time_delivery(shipments: List[Shipment]) -> float
│   │       │                         # def calculate_carrier_performance(carrier_id: str) -> CarrierPerformance
│   │       │                         # def calculate_supplier_otif(supplier_id: str) -> OTIFScore
│   │       │                         # class CarrierPerformance(on_time_rate: float, damage_rate: float, cost_efficiency: float)
│   │       │                         # class OTIFScore(on_time: float, in_full: float, overall: float)
│   │       │
│   │       └── dashboard.py          # class DashboardMetrics
│   │                               # def get_real_time_metrics() -> RealTimeMetrics
│   │                               # def get_historical_trends(metric: str, period: DateRange) -> TrendData
│   │                               # class RealTimeMetrics(pending_orders: int, in_transit_shipments: int, low_stock_items: int, system_health: str)
│   │
│   ├── simulation/                   # Simulation engine for what-if scenarios
│   │   ├── __init__.py
│   │   │
│   │   ├── engine.py                 # class SimulationEngine
│   │   │   │                         # def simulate_supply_chain(events: List[SimulationEvent], duration_days: int) -> SimulationResult
│   │   │   │                         # def simulate_demand_scenario(demand_profile: DemandProfile, inventory_levels: Dict[str, int]) -> ScenarioResult
│   │   │   │                         # def simulate_disruption_scenario(disruption: DisruptionEvent, network: SupplyChainNetwork) -> DisruptionImpact
│   │   │   │                         # class SimulationResult(metrics: SimulationMetrics, events: List[SimulatedEvent], recommendations: List[Recommendation])
│   │   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── events.py             # class SimulationEvent(event_type: str, timestamp: datetime, parameters: Dict[str, Any])
│   │   │   │                         # class DemandEvent(SimulationEvent): item_id: str, quantity: int
│   │   │   │                         # class SupplyEvent(SimulationEvent): item_id: str, quantity: int, supplier_id: str
│   │   │   │                         # class DisruptionEvent(SimulationEvent): disruption_type: DisruptionType, affected_entities: List[str], duration_hours: int
│   │   │   │                         # enum DisruptionType: PORT_CLOSURE, SUPPLIER_FAILURE, TRANSPORTATION_STRIKE, NATURAL_DISASTER
│   │   │   │
│   │   │   └── network.py            # class SupplyChainNetwork(nodes: List[NetworkNode], edges: List[NetworkEdge])
│   │   │                           # class NetworkNode(node_id: str, node_type: NodeType, capacity: float, location: Location)
│   │   │                           # class NetworkEdge(from_node: str, to_node: str, capacity: float, lead_time: float, cost: Decimal)
│   │   │                           # enum NodeType: WAREHOUSE, SUPPLIER, DISTRIBUTION_CENTER, RETAILER
│   │   │
│   │   └── scenarios/
│   │       ├── __init__.py
│   │       ├── demand_surge.py       # def create_demand_surge_scenario(surge_percentage: float, duration_days: int) -> List[SimulationEvent]
│   │       ├── supplier_failure.py   # def create_supplier_failure_scenario(supplier_id: str, recovery_time_days: int) -> List[SimulationEvent]
│   │       └── port_disruption.py    # def create_port_disruption_scenario(port_id: str, duration_days: int) -> List[SimulationEvent]
│   │
│   └── config/                       # Configuration management
│       ├── __init__.py
│       ├── settings.py              # class Settings(BaseSettings)
│       │                           # database_url: str
│       │                           # redis_url: str
│       │                           # rabbitmq_url: str
│       │                           # log_level: str
│       │                           # environment: str
│       │                           # secret_key: str
│       │
│       ├── database.py              # class DatabaseConfig
│       │                           # host: str
│       │                           # port: int
│       │                           # database: str
│       │                           # username: str
│       │                           # password: str
│       │
│       ├── logging.py               # class LoggingConfig
│       │                           # level: str
│       │                           # format: str
│       │                           # handlers: List[HandlerConfig]
│       │
│       └── features.py              # class FeatureFlags
│                                   # enable_simulation: bool
│                                   # enable_advanced_analytics: bool
│                                   # enable_ml_forecasting: bool
│                                   # enable_real_time_tracking: bool
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration and fixtures
│   │                             # @pytest.fixture def db_session()
│   │                             # @pytest.fixture def inventory_service()
│   │                             # @pytest.fixture def order_service()
│   │
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── test_inventory.py   # class TestItem, TestStockLevel, TestInventoryService
│   │   │   │                     # def test_create_item()
│   │   │   │                     # def test_adjust_stock_insufficient()
│   │   │   │                     # def test_reserve_stock_success()
│   │   │   │
│   │   │   ├── test_supplier.py    # class TestSupplier, TestSupplierScore, TestScoreCalculator
│   │   │   │                     # def test_register_supplier()
│   │   │   │                     # def test_reliability_score_calculation()
│   │   │   │
│   │   │   ├── test_order.py        # class TestOrder, TestOrderService, TestOrderValidator
│   │   │   │                     # def test_create_order()
│   │   │   │                     # def test_process_order_insufficient_stock()
│   │   │   │                     # def test_cancel_order()
│   │   │   │
│   │   │   ├── test_transportation.py # class TestRoute, TestShipment, TestRoutingEngine
│   │   │   │                     # def test_plan_route()
│   │   │   │                     # def test_find_shortest_path()
│   │   │   │
│   │   │   └── test_warehouse.py    # class TestWarehouse, TestWarehouseService
│   │   │                           # def test_register_warehouse()
│   │   │                           # def test_allocate_storage()
│   │   │
│   │   └── application/
│   │       ├── __init__.py
│   │       ├── test_use_cases/
│   │       │   ├── __init__.py
│   │       │   ├── test_create_item.py # class TestCreateItemUseCase
│   │       │   │                     # def test_execute_success()
│   │       │   │                     # def test_execute_invalid_sku()
│   │       │   │
│   │       │   ├── test_create_order.py # class TestCreateOrderUseCase
│   │       │   │                     # def test_execute_success()
│   │       │   │                     # def test_execute_insufficient_stock()
│   │       │   │
│   │       │   └── test_process_order.py # class TestProcessOrderUseCase
│   │       │                           # def test_execute_success()
│   │       │                           # def test_execute_invalid_status()
│   │       │
│   │       └── test_workflows/
│   │           ├── __init__.py
│   │           └── test_order_fulfillment.py # class TestOrderFulfillmentWorkflow
│   │                                               # def test_execute_end_to_end()
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_inventory_repository.py # class TestSQLInventoryRepository
│   │   │                                 # async def test_save_and_retrieve_item()
│   │   │                                 # async def test_update_stock_level()
│   │   │
│   │   ├── test_order_repository.py # class TestSQLOrderRepository
│   │   │                           # async def test_save_and_retrieve_order()
│   │   │
│   │   └── test_api_endpoints.py   # class TestAPIEndpoints
│   │                               # async def test_create_item_endpoint()
│   │                               # async def test_create_order_endpoint()
│   │                               # async def test_track_shipment_endpoint()
│   │
│   └── performance/
│       ├── __init__.py
│       ├── test_load.py             # class TestLoadScenarios
│       │                           # async def test_concurrent_order_creation()
│       │                           # async def test_bulk_inventory_update()
│       │
│       └── test_scalability.py      # class TestScalability
│                                   # async def test_large_dataset_query()
│                                   # async def test_memory_usage()
│
├── scripts/                        # Utility and maintenance scripts
│   ├── __init__.py
│   ├── seed_data.py                # async def main() -> None
│   │                             # Script to populate database with sample data
│   │
│   ├── migrate.py                  # async def main() -> None
│   │                             # Database migration runner
│   │
│   ├── generate_report.py           # async def main() -> None
│   │                             # Generate scheduled reports
│   │
│   └── cleanup.py                   # async def main() -> None
│                               # Cleanup old data and logs
│
├── docs/                           # Documentation
│   ├── architecture.md             # System architecture documentation
│   ├── api.md                      # API documentation
│   ├── deployment.md               # Deployment guide
│   ├── development.md               # Development setup guide
│   └── domain_models.md            # Domain model documentation
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Continuous integration pipeline
│       ├── cd.yml                  # Continuous deployment pipeline
│       └── test.yml                # Test automation
│
└── monitoring/                     # Monitoring and observability
    ├── prometheus.yml              # Prometheus configuration
    ├── grafana/
    │   └── dashboards/
    │       ├── inventory.json      # Grafana dashboard for inventory metrics
    │       ├── orders.json         # Grafana dashboard for order metrics
    │       └── performance.json    # Grafana dashboard for performance metrics
    └── alerts/
        └── alerts.yml              # Alerting rules
```

## Key Architecture Principles

### Clean Architecture Layers
1. **Domain Layer**: Pure business logic, no external dependencies
2. **Application Layer**: Use cases and orchestration
3. **Infrastructure Layer**: External systems implementation
4. **Interfaces Layer**: API, CLI, and external interfaces

### Design Patterns Used
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic encapsulation
- **DTO Pattern**: Data transfer objects for interfaces
- **Factory Pattern**: Object creation
- **Strategy Pattern**: Pluggable algorithms (forecasting, optimization)
- **Observer Pattern**: Domain events and handlers
- **Dependency Injection**: Loose coupling

### Type Hints Strategy
- All functions use type annotations
- Domain models use dataclasses or Pydantic
- Repository interfaces use abstract base classes
- Use cases have explicit Request/Response DTOs
- Generic types for collections (List, Dict, Optional)

### Scalability Features
- Async/await throughout for I/O operations
- Caching layer (Redis)
- Message queue (RabbitMQ) for async processing
- Database connection pooling
- Horizontal scaling ready (stateless services)
- Rate limiting and middleware

### Advanced Capabilities
- **Risk Scoring**: Multi-factor risk assessment for suppliers and inventory
- **Optimization**: Route optimization, inventory optimization, cost optimization
- **Forecasting**: Demand forecasting with multiple algorithms
- **Simulation**: What-if scenario modeling
- **Analytics**: KPI calculation, reporting, dashboards
- **Real-time Tracking**: Shipment tracking and status updates
