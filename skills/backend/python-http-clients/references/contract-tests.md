# HTTPX transport tests and provider contract verification

**Read when:** writing deterministic async HTTP tests, provider error classification, or staging integration verification.

## MockTransport, not real internet in unit tests

~~~python
import httpx
import pytest
from pydantic import BaseModel

class Resource(BaseModel):
    id: int
    name: str

@pytest.mark.anyio
async def test_httpx_adapter_parses_valid_payload():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/resources/1"
        return httpx.Response(200, json={"id": 1, "name": "sample"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        base_url="https://partner.example", transport=transport
    ) as http:
        from app.clients.partner import ExternalApiClient
        result = await ExternalApiClient(http).get_model("/resources/1", Resource)
        assert result.name == "sample"
~~~

This references the example adapter module from the caller's application; adapt imports to the real project. It requires pytest and an anyio backend fixture/plugin; a real repo should pin versions and supply its anyio backend where needed.

## Failure injection matrix

| Case | Test | Expected |
|---|---|---|
| Unauthorized | Mock 401 | Nonretryable auth failure, no raw token in public error |
| Not found | Mock 404 | Business/application mapping according to contract |
| Throttled | Mock 429 + header | Budgeted backoff or typed rate limit |
| Server failure | Mock 503 | Bounded retry only if safe |
| Invalid JSON | Mock 200 broken body | Protocol/schema exception |
| Valid JSON wrong fields | Mock unexpected schema | ValidationError mapping |
| Network | Mock transport raise ConnectError | Transient network error |
| Timeout | Simulate timeout subclass | Classified and bounded |
| Retry after commit | First call performs side effect then timeout | Durable idempotency or reconciliation |
| Cancellation | Cancel in-flight request | Propagates, resources closed |

Unit tests can't prove partner credential/region/TLS or live error schema behavior; run opt-in integration against a sandbox with minimum-privilege account and no destructive calls.

## Stable public contract
Record exact API version, documented request/response schema, rate limits and deprecation policy. For APIs without schema, use tolerant reading of additive fields where safe and strict validation of fields business relies on.

Official: https://www.python-httpx.org/advanced/transports/ and https://docs.pytest.org/en/stable/how-to/fixtures.html .
