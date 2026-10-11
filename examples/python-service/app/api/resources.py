import httpx
from fastapi import APIRouter, Depends, Request

from app.clients.external import ExternalApiClient
from app.services.resource import ResourceService
from app.models import ResourceResponse

router = APIRouter()

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.external_http

def get_resource_service(http: httpx.AsyncClient = Depends(get_http_client)) -> ResourceService:
    return ResourceService(ExternalApiClient(http))

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def resource(
    resource_id: int,
    service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    return await service.get_resource(resource_id)
