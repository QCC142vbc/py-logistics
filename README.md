# Logistics Management System

A comprehensive, production-ready Python logistics management system built with clean architecture principles.

## Features

- **Inventory Management**: Track items, stock levels, and transactions
- **Supplier Management**: Manage suppliers, contracts, and performance scoring
- **Order Processing**: Handle customer orders and purchase orders
- **Transportation**: Route planning, shipment tracking, carrier management
- **Warehouse Management**: Storage allocation, transfers, utilization
- **Advanced Analytics**: Risk scoring, optimization, forecasting, reporting
- **Simulation Engine**: What-if scenario modeling

## Architecture

This project follows clean architecture principles with clear separation of concerns:

- **Domain Layer**: Pure business logic (no external dependencies)
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External systems implementation
- **Interfaces Layer**: API, CLI, and external interfaces

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- RabbitMQ 3.12+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run database migrations
python scripts/migrate.py

# Seed initial data
python scripts/seed_data.py
```

### Running the Application

```bash
# Start the API server
uvicorn src.interfaces.api.main:app --reload

# Run the CLI
python -m src.interfaces.cli.main --help
```

## Testing

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src --cov-report=html
```

## Development

See [docs/development.md](docs/development.md) for detailed development guidelines.

## License

MIT
