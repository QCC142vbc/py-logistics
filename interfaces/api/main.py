from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interfaces.api.routes import inventory, orders, suppliers, shipments, warehouses, analytics
from src.config.settings import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Logistics Management System API",
        description="A comprehensive logistics management system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
    app.include_router(suppliers.router, prefix="/api/v1/suppliers", tags=["suppliers"])
    app.include_router(shipments.router, prefix="/api/v1/shipments", tags=["shipments"])
    app.include_router(warehouses.router, prefix="/api/v1/warehouses", tags=["warehouses"])
    app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "environment": settings.environment}

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": "Logistics Management System",
            "version": "1.0.0",
            "docs": "/docs",
        }

    return app


def get_application() -> FastAPI:
    """Get the configured FastAPI application."""
    return create_app()


app = get_application()
