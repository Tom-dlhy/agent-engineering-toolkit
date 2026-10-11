from typing import Protocol

from app.models import ResourceResponse
from app.errors import ResourceNotFound

class ResourceReader(Protocol):
    async def get_resource(self, resource_id: int) -> ResourceResponse: ...

class ResourceService:
    def __init__(self, reader: ResourceReader) -> None:
        self.reader = reader

    async def get_resource(self, resource_id: int) -> ResourceResponse:
        if resource_id < 1:
            raise ResourceNotFound("invalid resource id")
        return await self.reader.get_resource(resource_id)
