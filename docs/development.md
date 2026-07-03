# Development Guide

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Copy environment file:
   ```bash
   cp .env.example .env
   ```

4. Start services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

5. Run migrations:
   ```bash
   alembic upgrade head
   ```

6. Seed database:
   ```bash
   python scripts/seed_data.py
   ```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run unit tests only:
```bash
pytest -m unit
```

### Run integration tests:
```bash
pytest -m integration
```

### Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Code Quality

### Format code:
```bash
black src/
```

### Check linting:
```bash
ruff check src/
```

### Type checking:
```bash
mypy src/
```

### Run all quality checks:
```bash
black src/ && ruff check src/ && mypy src/
```

## Running the Application

### API Server:
```bash
uvicorn src.interfaces.api.main:app --reload
```

### CLI:
```bash
python -m src.interfaces.cli.main --help
```

## Adding New Features

### 1. Add Domain Model

Create model in `src/domain/{module}/models.py`:

```python
from dataclasses import dataclass
from src.domain.common.models import Entity

@dataclass
class NewEntity(Entity):
    name: str
    value: int
```

### 2. Add Repository Interface

Create in `src/domain/{module}/repository.py`:

```python
from abc import ABC, abstractmethod

class NewEntityRepository(ABC):
    @abstractmethod
    async def get(self, id: str):
        pass
```

### 3. Implement Repository

Create in `src/infrastructure/database/repositories/`:

```python
class SQLNewEntityRepository(NewEntityRepository):
    async def get(self, id: str):
        # Implementation
        pass
```

### 4. Add Use Case

Create in `src/application/use_cases/{module}/`:

```python
class CreateEntityUseCase:
    async def execute(self, request):
        # Implementation
        pass
```

### 5. Add API Endpoint

Create in `src/interfaces/api/routes/{module}.py`:

```python
@router.post("/")
async def create_entity(request: Request):
    # Implementation
    pass
```

## Database Migrations

### Create migration:
```bash
alembic revision --autogenerate -m "description"
```

### Apply migration:
```bash
alembic upgrade head
```

### Rollback migration:
```bash
alembic downgrade -1
```

## Debugging

### Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

### Use pdb:
```python
import pdb; pdb.set_trace()
```

### Use VS Code debugger:
- Set breakpoints in code
- Run with debugger attached

## Common Issues

### Database connection failed
- Check Docker Compose services are running
- Verify DATABASE_URL in .env

### Tests failing
- Ensure test database is clean
- Check fixtures in conftest.py

### Import errors
- Ensure PYTHONPATH includes src/
- Run from project root
