# FastAPI testing and production readiness

**Read when:** writing pytest tests, integration/contract checks, configuring workers or preparing production launch.

## Test pyramid for HTTP services

- Unit: pure service rules with fake adapters, expected exceptions and no real network.
- API: TestClient lifespan and dependency overrides for status, DTO, auth and error contract; negative invalid input tests.
- Adapter integration: HTTPX MockTransport or external mock server and real ephemeral database where needed.
- End-to-end: one critical request from HTTP through real adapters; don't claim unit mocks prove IAM/SQL.
- Concurrency/failure: simultaneous PATCH, pool saturation, timeout, network denial, duplicate POST, worker restart, slow LLM.
- Security: tenant scoping, invalid token, SSRF allowlist, log redaction, body/input limits.

~~~python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
~~~

A skeleton only; actual resource tests must set deterministic dependencies and test exact behavior, not just status.

## Readiness and deployment

Set health/readiness contracts, startup config validation, lifecycle cleanup, graceful SIGTERM handling, structured logs, OTel, rate limits, auth+tenant checks and DB migrations as separate controlled deployment action. Proxy/load balancer timeout must exceed allowed request budget consistently; bound outbound deadlines to leave enough time for response.

Scale by measured p95/99 and connection budgets. ASGI workers multiply per-process HTTPX/DB pool sizes. Don't run schema migrations automatically in every replica startup. Critical long jobs should leave the request path and use durable queues.

## Example check commands

~~~bash
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked mypy app
uv run --locked uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

The commands assume the project uses uv and those dependencies; preserve repo conventions. Test a production-like image/build, health and graceful shutdown in staging before claiming ready.

Official: https://fastapi.tiangolo.com/tutorial/testing/ and https://fastapi.tiangolo.com/deployment/ and https://www.python-httpx.org/advanced/transports/ .
