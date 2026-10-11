# FastAPI lifespan, clients and DI

**Read when:** initializing/closing HTTPX clients, database pools, LLM SDKs or configuring tests and dependencies.

## Scope ownership

One ASGI process creates a **shared** HTTPX connection pool and SQLAlchemy engine at startup, disposes on shutdown; a **request** creates its own AsyncSession / domain service; a **task** owns its own transient state. Multiprocess workers each have independent pools, increasing total connections.

~~~python
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request, Depends

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        base_url="https://api.example.org",
        timeout=httpx.Timeout(10.0, connect=2, pool=2),
        limits=httpx.Limits(max_connections=50, max_keepalive_connections=15),
    ) as client:
        app.state.external_http = client
        yield

app = FastAPI(lifespan=lifespan)

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.external_http

@app.get("/health")
async def health():
    return {"status": "ok"}
~~~

Never use a real arbitrary external URL in a deployment without verifying allowlisted endpoints/TLS. This example illustrates lifetime; it is not a complete API/auth service. Prefer composition at app factory rather than import-time network connection.

## Inject application service

~~~python
from typing import Annotated
from fastapi import Depends

def get_service(client: Annotated[httpx.AsyncClient, Depends(get_http_client)]):
    return ResourceService(ExternalApiClient(client))
~~~

Keep `ResourceService` free of FastAPI Request and vendor status codes; type its injected port. For expensive/durable adapters initialize in lifespan, but do not store mutable request-specific authorization in global app.state.

## Async versus sync

If the underlying client is blocking, use sync endpoints or thread offload with a bounded executor; simply writing async def doesn't make boto3 or an ORM synchronous connection nonblocking. When using async DB driver and SQLAlchemy AsyncSession, one session per request/task, close promptly. A long-held transaction across outbound LLM/HTTP call can exhaust locks/pool.

## Readiness

Liveness proves process responsive; readiness can assess critical local dependencies with bounded deadlines. Avoid making health endpoint query every third-party model synchronously, creating amplification; use separate dependency diagnostics and operator alarms.

## Tests

Use `with TestClient(app)` to trigger lifespan, or ASGITransport plus LifespanManager (appropriate third-party test utility) for async tests; HTTPX ASGITransport alone does not guarantee lifespan. Override dependencies for deterministic unit tests, use real sandbox adapters for integration, and ensure cleanup/overrides reset.

Official: https://fastapi.tiangolo.com/advanced/events/ and https://fastapi.tiangolo.com/tutorial/dependencies/ and https://www.python-httpx.org/async/ .
