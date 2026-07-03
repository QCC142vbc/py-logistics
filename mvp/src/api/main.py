from fastapi import FastAPI
from src.api.routes import router
from src.repositories.repository import get_repository

app = FastAPI(title="Logistics MVP", version="1.0.0")

app.include_router(router)


@app.on_event("startup")
async def startup():
    repo = get_repository()
    await repo.create_tables()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {
        "message": "Logistics MVP API",
        "docs": "/docs",
        "health": "/health"
    }
