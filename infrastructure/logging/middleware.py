from fastapi import Request


class LoggingMiddleware:
    def __init__(self, logger) -> None:
        self._logger = logger

    async def log_request(self, request: Request) -> None:
        """Log incoming request."""
        self._logger.info(
            f"Incoming request",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

    async def log_response(self, response) -> None:
        """Log outgoing response."""
        self._logger.info(
            f"Response sent",
            status_code=response.status_code,
        )
