import uuid
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.resources import router
from app.core.context import correlation_id_var
from app.core.settings import get_settings
from app.errors import (
    ResourceNotFound, ExternalUnavailable,
    ExternalProtocolError, ExternalRateLimited,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()  # missing required URL fails before serving
    async with httpx.AsyncClient(
        base_url=str(settings.external_api_url),
        timeout=httpx.Timeout(settings.external_api_timeout, connect=2, pool=2),
        limits=httpx.Limits(max_connections=30, max_keepalive_connections=10),
        follow_redirects=False,
    ) as client:
        app.state.external_http = client
        yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.middleware("http")
async def set_correlation_id(request: Request, call_next):
    incoming = request.headers.get("X-Correlation-ID", "")
    allowed = 0 < len(incoming) <= 128 and all(ch.isalnum() or ch in "-_" for ch in incoming)
    value = incoming if allowed else str(uuid.uuid4())
    token = correlation_id_var.set(value)
    try:
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = value
        return response
    finally:
        correlation_id_var.reset(token)

def safe_error(code: str, status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content={"code": code, "detail": code.replace("_", " ")})

@app.exception_handler(ResourceNotFound)
async def missing(request: Request, exc: ResourceNotFound):
    return safe_error("resource_not_found", 404)

@app.exception_handler(ExternalRateLimited)
async def limited(request: Request, exc: ExternalRateLimited):
    return safe_error("external_rate_limited", 503)

@app.exception_handler(ExternalUnavailable)
async def unavailable(request: Request, exc: ExternalUnavailable):
    return safe_error("external_unavailable", 503)

@app.exception_handler(ExternalProtocolError)
async def bad_provider(request: Request, exc: ExternalProtocolError):
    return safe_error("external_protocol_error", 502)
