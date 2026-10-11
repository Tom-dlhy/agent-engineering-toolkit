# HTTPX reusable async client with Pydantic response contracts

**Read when:** implementing typed outbound API calls, AsyncClient pooling, correlation propagation or status mapping.

## Client and configuration

~~~python
import httpx

def build_client(base_url: str) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=base_url, follow_redirects=False,
        timeout=httpx.Timeout(10.0, connect=2.0, read=8.0, write=5.0, pool=2.0),
        limits=httpx.Limits(max_connections=40, max_keepalive_connections=10),
    )
~~~

Choose actual timeout/pool budgets based on provider latency, pool wait and upstream limits; sample values are placeholders, not SLO recommendations. Construct and dispose at FastAPI lifespan or worker startup/shutdown. An allowed fixed base URL and non-user-controlled path defend against SSRF; TLS verification on by default.

## Typed response parsing and error separation

~~~python
import logging
from typing import TypeVar
import httpx
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)

class UpstreamUnavailable(Exception): pass
class UpstreamProtocolError(Exception): pass
class UpstreamNotFound(Exception): pass
class UpstreamRateLimited(Exception): pass

class ExternalApiClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_model(self, path: str, model: type[T]) -> T:
        try:
            response = await self.client.get(path)
        except httpx.TimeoutException as exc:
            raise UpstreamUnavailable("timeout") from exc
        except httpx.RequestError as exc:
            raise UpstreamUnavailable("network") from exc

        if response.status_code == 404:
            raise UpstreamNotFound(path)
        if response.status_code == 429:
            raise UpstreamRateLimited("throttled")
        if response.status_code >= 500:
            raise UpstreamUnavailable("provider 5xx")
        if response.is_error:
            raise UpstreamProtocolError(f"unexpected status {response.status_code}")
        try:
            return model.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise UpstreamProtocolError("invalid response") from exc
~~~

Whether upstream 404 maps to app 404 depends on business identity: e.g. a missing partner record may be user-visible, whereas a 404 from a misconfigured model route is an integration fault. Status 401/403 usually means credentials/entitlements and should not be retried. Log sanitized method, route template, elapsed time, safe status and trace ID at one structured boundary; no response bodies, cookies, authorization header, secret query strings or PII.

## Correlation and trust

Propagate generated/validated correlation ID as an optional X-Correlation-ID header only to approved upstream partner APIs. Don't let untrusted headers override Authorization. For tracing use W3C trace context under your security policy and OTel library.

## Errors and evidence

Contract tests should include success, 404, 401, 429, 500, invalid JSON, invalid schema, connect/read/pool timeout, redirect and cancellation. A correct HTTP return code does not guarantee semantically valid data; always parse the response.

Official: https://www.python-httpx.org/async/ and https://www.python-httpx.org/advanced/timeouts/ and https://www.python-httpx.org/advanced/resource-limits/ .
