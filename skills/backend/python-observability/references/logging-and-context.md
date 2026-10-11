# Python JSON logging, request contexts and data minimization

**Read when:** implementing structured logs or correlation propagation in async Python services.

~~~python
import json
import logging
from datetime import datetime, timezone
from contextvars import ContextVar

request_id: ContextVar[str | None] = ContextVar("request_id", default=None)

class JsonFormatter(logging.Formatter):
    allowed_extra = ("event", "method", "route", "status_code", "duration_ms")

    def format(self, record: logging.LogRecord) -> str:
        data: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if (value := request_id.get()) is not None:
            data["request_id"] = value
        for name in self.allowed_extra:
            value = getattr(record, name, None)
            if value is not None:
                data[name] = value
        if record.exc_info:
            # Only in access-controlled internal logs, with scrubber.
            data["exception_type"] = record.exc_info[0].__name__
        return json.dumps(data, ensure_ascii=False, default=str)
~~~

Formatter reads a ContextVar in handler execution context; frameworks or logging queues can move formatting to another task/thread and lose it. For asynchronous handlers/queues, consider capturing context into LogRecord at emission via a filter/factory, test concurrency and worker propagation.

## Configure once, not at import

~~~python
def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
~~~

Global handler reset is appropriate for a standalone app's explicit bootstrap only; it may disrupt an existing app, test runner or hosting server that manages logging. Avoid secret-bearing stack frames, raw request paths with tokens, credentials and LLM prompt content.

## Context safety
Generate validated short request ID for incoming request; set ContextVar with token and reset in finally; propagate to known downstream only. A request ID is never authentication. Workers/retries/jobs need an explicit business correlation ID in durable payload because process-local ContextVar does not survive a queue boundary.

## Negative tests
Concurrent requests don't swap IDs, exception contains safe type only, malformed header filtered, missing context emits no field, streaming background task behavior explicit, no Authorization/Cookie/raw URL data.

Official: https://docs.python.org/3/library/logging.html and https://docs.python.org/3/library/contextvars.html .
