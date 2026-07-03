from dataclasses import dataclass
from typing import List


@dataclass
class HandlerConfig:
    """Logging handler configuration."""
    type: str  # console, file
    level: str
    format: str


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "json"
    handlers: List[HandlerConfig] = None

    def __post_init__(self) -> None:
        if self.handlers is None:
            self.handlers = [
                HandlerConfig(type="console", level="INFO", format="json")
            ]
