from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from src.domain.common.exceptions import DomainException


async def handle_domain_exception(request: Request, exc: DomainException) -> JSONResponse:
    """Handle domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.message,
            "type": exc.__class__.__name__,
            "details": exc.details,
        },
    )


async def handle_validation_exception(request: Request, exc: Exception) -> JSONResponse:
    """Handle validation exceptions."""
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": str(exc)},
    )


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
