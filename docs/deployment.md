# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- RabbitMQ 3.12+

## Local Development

### Using Docker Compose

1. Clone the repository
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Start services:
   ```bash
   docker-compose up -d
   ```
4. Run migrations:
   ```bash
   docker-compose exec app alembic upgrade head
   ```
5. Seed database:
   ```bash
   docker-compose exec app python scripts/seed_data.py
   ```
6. Access API at `http://localhost:8000`

### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL:
   ```bash
   createdb logistics_db
   ```

3. Configure environment variables in `.env`

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Seed database:
   ```bash
   python scripts/seed_data.py
   ```

6. Start API server:
   ```bash
   uvicorn src.interfaces.api.main:app --reload
   ```

## Production Deployment

### Using Docker

1. Build image:
   ```bash
   docker build -t logistics-system:latest .
   ```

2. Run with production environment:
   ```bash
   docker run -d \
     -p 8000:8000 \
     --env-file .env.production \
     logistics-system:latest
   ```

### Using Kubernetes

See `kubernetes/` directory for manifests.

### Environment Variables

Required production variables:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
RABBITMQ_URL=amqp://user:pass@host:5672/
SECRET_KEY=your-production-secret-key
ENVIRONMENT=production
DEBUG=false
```

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Logs

Logs are structured JSON. Use a log aggregator like:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Grafana Loki
- CloudWatch Logs

### Metrics

Prometheus metrics can be added using `prometheus-fastapi-instrumentator`.

## Backup

### Database Backup

```bash
pg_dump logistics_db > backup.sql
```

### Restore

```bash
psql logistics_db < backup.sql
```

## Scaling

### Horizontal Scaling

- Use a load balancer (nginx, AWS ALB)
- Deploy multiple API instances
- Use shared Redis for caching
- Use PostgreSQL read replicas for read-heavy workloads

### Vertical Scaling

- Increase database resources
- Add Redis cluster for caching
- Use message queue for async processing
