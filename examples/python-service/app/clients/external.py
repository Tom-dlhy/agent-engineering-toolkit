import httpx
from pydantic import ValidationError

from app.models import ResourceResponse
from app.errors import (
    ResourceNotFound, ExternalUnavailable,
    ExternalProtocolError, ExternalRateLimited,
)
from app.core.context import correlation_id_var

class ExternalApiClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self.http = http

    async def get_resource(self, resource_id: int) -> ResourceResponse:
        correlation = correlation_id_var.get()
        headers = {"X-Correlation-ID": correlation} if correlation else {}
        try:
            response = await self.http.get(f"/resources/{resource_id}", headers=headers)
        except httpx.TimeoutException as exc:
            raise ExternalUnavailable("upstream timeout") from exc
        except httpx.RequestError as exc:
            raise ExternalUnavailable("upstream connection") from exc

        if response.status_code == 404:
            raise ResourceNotFound("resource absent")
        if response.status_code == 429:
            raise ExternalRateLimited("provider limited")
        if response.status_code >= 500:
            raise ExternalUnavailable("upstream 5xx")
        if response.is_error:
            raise ExternalProtocolError("unexpected status")
        try:
            return ResourceResponse.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise ExternalProtocolError("invalid upstream payload") from exc
