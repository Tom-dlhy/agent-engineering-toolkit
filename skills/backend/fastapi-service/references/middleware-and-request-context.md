# FastAPI request IDs, trusted context and logging

**Read when:** implementing correlation IDs, logging middleware, request metrics or propagation across HTTP/LLM calls.

## Correlation ID: propagation is not authentication

Incoming X-Correlation-ID is untrusted client input. Accept only bounded safe formats (e.g. UUID or <=128 characters restricted to alphanumeric/-/_), otherwise mint a new ID. Use W3C traceparent for distributed traces separately when tracing is available; correlation IDs do not replace traces.

~~~python
import uuid
from contextvars import ContextVar
from fastapi import Request

correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)

@app.middleware("http")
async def correlate(request: Request, call_next):
    raw = request.headers.get("X-Correlation-ID", "")
    good = 0 < len(raw) <= 128 and all(c.isalnum() or c in "-_" for c in raw)
    value = raw if good else str(uuid.uuid4())
    token = correlation_id.set(value)
    try:
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = value
        return response
    finally:
        correlation_id.reset(token)
~~~

This pattern is appropriate for ordinary request logs, but framework middleware/task boundaries, background work and sync thread offload can affect context propagation. Test it end-to-end; logging filters that run later in another context may not see expected value. Never put customer input into logger fields without sanitization.

## Structured logs

Use JSON formatter or stdlib logging integration with timestamp UTC, level, logger, event, request_id, trace_id, method, route template (avoid raw query strings), duration and outcome; redact tokens, Authorization, cookies, PII and provider prompt/response by default. Exception traceback may contain secrets; restrict logs and retention. No raw LLM tool input or signed URL.

## Middleware performance and correctness

Record duration with monotonic clock, capture status on HTTPException/unhandled paths, note streaming response timing semantics (header sending vs stream completion). Do not swallow CancelledError; avoid expensive logging JSON on hot path. Test concurrent requests do not leak IDs between ContextVar contexts; duplicate header, excessively long/malformed value, exception path and HEAD/stream routes.

## Distributed tracing

If OTel is deployed, attach trace/span IDs from current span, instrument outbound HTTPX/DB and propagate authorized trace headers. Avoid implementing a competing tracing protocol with only X-Correlation-ID.

Official: https://fastapi.tiangolo.com/tutorial/middleware/ and https://docs.python.org/3/library/contextvars.html and https://www.w3.org/TR/trace-context/ .
