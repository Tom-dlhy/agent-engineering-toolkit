import json
import logging
from datetime import datetime, timezone

from .context import correlation_id_var

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if (value := correlation_id_var.get()) is not None:
            data["correlation_id"] = value
        for key in ("event", "method", "route", "status_code"):
            if (value := getattr(record, key, None)) is not None:
                data[key] = value
        if record.exc_info:
            data["exception_type"] = record.exc_info[0].__name__
        return json.dumps(data, ensure_ascii=False)

def configure_logging(level: str = "INFO") -> None:
    # Call only at application bootstrap when the host doesn't own logging.
    root = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.handlers[:] = [handler]
    root.setLevel(level)
