from collections.abc import Callable
import pytest
import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.api.resources import get_http_client
from app.core.settings import get_settings
from app.core.context import correlation_id_var

@pytest.fixture
def build_client(monkeypatch):
    monkeypatch.setenv("APP_EXTERNAL_API_URL", "https://partner.example.org/")
    get_settings.cache_clear()
    clients: list[httpx.AsyncClient] = []

    def factory(handler: Callable[[httpx.Request], httpx.Response]) -> TestClient:
        upstream = httpx.AsyncClient(
            base_url="https://partner.example.org",
            transport=httpx.MockTransport(handler),
        )
        clients.append(upstream)
        app.dependency_overrides[get_http_client] = lambda: upstream
        return TestClient(app)

    yield factory
    app.dependency_overrides.clear()
    import asyncio
    for client in clients:
        asyncio.run(client.aclose())
    get_settings.cache_clear()

def test_health_without_upstream_request(build_client):
    def unexpected(req):
        raise AssertionError("health should not contact partner")
    with build_client(unexpected) as test:
        response = test.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_valid_response_and_correlation(build_client):
    seen: list[str] = []
    def provider(req):
        seen.append(req.headers.get("X-Correlation-ID", ""))
        return httpx.Response(200, json={"id": 3, "name": "example"})
    with build_client(provider) as test:
        response = test.get("/resources/3", headers={"X-Correlation-ID": "request_42"})
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "example"}
    assert response.headers["X-Correlation-ID"] == "request_42"
    assert seen == ["request_42"]
    assert correlation_id_var.get() is None

@pytest.mark.parametrize(("code", "expected"), [(404, 404), (429, 503), (503, 503), (403, 502)])
def test_upstream_http_error_mapping(build_client, code, expected):
    with build_client(lambda req: httpx.Response(code)) as test:
        response = test.get("/resources/3")
    assert response.status_code == expected
    assert "code" in response.json()

def test_upstream_invalid_json_is_502(build_client):
    with build_client(lambda req: httpx.Response(200, text="not-json")) as test:
        response = test.get("/resources/3")
    assert response.status_code == 502

def test_upstream_invalid_schema_is_502(build_client):
    with build_client(lambda req: httpx.Response(200, json={"id": "wrong"})) as test:
        response = test.get("/resources/3")
    assert response.status_code == 502

def test_invalid_client_id_is_422(build_client):
    with build_client(lambda req: httpx.Response(200, json={"id": 3, "name": "x"})) as test:
        response = test.get("/resources/not-an-int")
    assert response.status_code == 422

def test_untrusted_header_replaced(build_client):
    def provider(req):
        assert "\n" not in req.headers.get("X-Correlation-ID", "")
        return httpx.Response(200, json={"id": 3, "name": "x"})
    with build_client(provider) as test:
        response = test.get("/resources/3", headers={"X-Correlation-ID": "x" * 200})
    assert response.status_code == 200
    assert len(response.headers["X-Correlation-ID"]) < 129

def test_network_failure_is_503(build_client):
    def provider(req):
        raise httpx.ConnectError("unreachable", request=req)
    with build_client(provider) as test:
        response = test.get("/resources/3")
    assert response.status_code == 503
