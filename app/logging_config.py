import json
import logging
import os
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    """Convierte cada registro de la aplicación en una línea JSON."""

    _extra_fields = (
        "event",
        "request_id",
        "method",
        "path",
        "status_code",
        "duration_ms",
    )

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in self._extra_fields:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> logging.Logger:
    """Configura el logger de SensorHub sin modificar loggers de dependencias."""
    logger = logging.getLogger("sensorhub")
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    logger.propagate = False
    return logger
