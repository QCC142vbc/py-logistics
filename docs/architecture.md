# Architecture Documentation

## Overview

The Logistics Management System follows Clean Architecture principles with clear separation of concerns across four main layers:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External dependencies (database, APIs, messaging)
- **Interfaces Layer**: External interfaces (CLI, REST API)

## Layer Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Interfaces Layer                      │
│  ┌──────────────┐           ┌──────────────┐           │
│  │     CLI      │           │  REST API    │           │
│  └──────────────┘           └──────────────┘           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Use Cases   │  │    DTOs      │  │  Workflows   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Domain Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Models     │  │  Repository  │  │   Services   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                Infrastructure Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Database   │  │   Cache      │  │   Messaging  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Domain Layer

### Modules

- **Inventory**: Item management, stock levels, transactions
- **Supplier**: Supplier management, scoring, contracts
- **Order**: Order lifecycle, purchase orders
- **Transportation**: Shipments, routes, carriers
- **Warehouse**: Storage locations, transfers
- **Common**: Shared value objects, exceptions
- **Events**: Domain events and event handling

### Key Patterns

- **Repository Pattern**: Abstract data access interfaces
- **Service Layer**: Business logic encapsulation
- **Value Objects**: Immutable domain concepts
- **Domain Events**: Event-driven architecture

## Application Layer

### Use Cases

Each use case represents a single business operation:

- `CreateItemUseCase`: Add new inventory items
- `AdjustStockUseCase`: Modify stock levels
- `CreateOrderUseCase`: Create customer orders
- `ProcessOrderUseCase`: Process and fulfill orders
- `RegisterSupplierUseCase`: Register new suppliers

### Workflows

Orchestrate multiple use cases:

- `OrderFulfillmentWorkflow`: Complete order-to-delivery process
- `ReplenishmentWorkflow`: Automatic inventory replenishment
- `WarehouseTransferWorkflow`: Inter-warehouse transfers

## Infrastructure Layer

### Database

- **ORM**: SQLAlchemy with async support
- **Database**: PostgreSQL
- **Migrations**: Alembic

### External Services

- **Cache**: Redis for performance optimization
- **Messaging**: RabbitMQ for async processing
- **Storage**: AWS S3 for document storage
- **APIs**: Carrier, payment gateway, geocoding

## Interfaces Layer

### CLI

Built with Typer and Rich for beautiful terminal output.

### REST API

Built with FastAPI, includes:
- OpenAPI documentation (Swagger UI)
- CORS middleware
- Error handling
- Request validation

## Analytics & Simulation

### Analytics

- **Risk Scoring**: Supplier and inventory risk assessment
- **Optimization**: Routing, inventory, cost optimization
- **Reporting**: Performance reports and dashboards
- **Forecasting**: Demand and lead time forecasting
- **Metrics**: KPI calculation and trends

### Simulation

- **What-if Scenarios**: Demand surges, disruptions
- **Network Modeling**: Supply chain network simulation
- **Event Simulation**: Disruption event modeling
