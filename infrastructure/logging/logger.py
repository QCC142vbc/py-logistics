import json
import logging
from dataclasses import dataclass
from typing import Any


@dataclass
class LoggingConfig:
    level: str = "INFO"
    format: str = "json"


class StructuredLogger:
    def __init__(self, name: str, config: LoggingConfig) -> None:
        self._name = name
        self._config = config
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, config.level))

        handler = logging.StreamHandler()
        if config.format == "json":
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        
        self._logger.addHandler(handler)

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(message, extra={"context": kwargs})

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(message, extra={"context": kwargs})

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(message, extra={"context": kwargs})

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(message, extra={"context": kwargs})


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        return json.dumps(log_data)
