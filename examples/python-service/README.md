# Minimal Python production-style FastAPI/HTTPX example

Purpose: executable, **educational vertical slice** of lifecycle-controlled HTTPX, Pydantic Settings, typed DTO, service/adapter boundary, safe error mapping and request correlation. It is NOT a production app ready to expose to users: no user authorization, persistence, rate limiting, real provider SLO integration, secrets backend or tracing exporter.

~~~bash
python -m pip install -e ".[dev]"
APP_EXTERNAL_API_URL=https://partner.example.org/ pytest -q
APP_EXTERNAL_API_URL=https://partner.example.org/ uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

For a real application: deploy behind authenticated gateway; validate external host configuration; add tenant authorization, SSL constraints, anti-SSRF, rate limiting and retries only after idempotency policy, DB transactions and OpenTelemetry. API GET /resources/{id} delegates to the configured upstream; the demo's URL must point to a safe authorized mock in tests.

Ownership: app/main.py lifespan creates HTTPX client once; api/resources.py handles HTTP; services/resource.py owns use-case boundary; clients/external.py maps provider protocol and validates response. Unit tests use HTTPX MockTransport, **no external network**.

For deployment/architecture choices see ../../docs/python-engineering-v2.md, and the V2 specialist skills.
