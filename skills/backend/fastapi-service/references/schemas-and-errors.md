# FastAPI request/response contracts, PATCH and errors

**Read when:** designing API validation, Create/Update/Response/List DTOs, partial changes or stable exception handling.

~~~python
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field

class ResourceStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class ResourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=200)
    status: ResourceStatus = ResourceStatus.ACTIVE

class ResourcePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=200)
    status: ResourceStatus | None = None

class ResourceResponse(BaseModel):
    resource_id: int
    name: str
    status: ResourceStatus

class ResourceListResponse(BaseModel):
    items: list[ResourceResponse]
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
~~~

## PATCH: omitted versus explicit null

`patch.model_dump(exclude_unset=True)` omits absent fields but **includes explicitly passed nulls**. Decide whether null clears, is forbidden or is meaningful for each field. For required nonnullable domain fields, reject explicit null (e.g. with Pydantic validator or service check); do not silently discard it via exclude_none=True. `mode="json"` serializes enums/dates for outbound JSON; domain operations should use Python types when possible. Concurrent PATCH can lose updates: use version/ETag conditional update or row locking where needed.

## Error taxonomy

| Internal condition | HTTP projection | Notes |
|---|---|---|
| Request shape invalid | 422 or existing contract's 400 | FastAPI defaults 422; be consistent |
| Auth/ownership denied | 401/403; sometimes masked 404 | Do not expose tenant existence |
| Resource missing | 404 | A provider 404 may be a legitimate business miss |
| State/optimistic concurrency conflict | 409 or 412 | Document version/ETag behavior |
| Rate limited | 429 | Retry-After only when meaningful |
| Upstream inaccessible | 502/503/504 depending ownership/failure | Avoid blanket 503 mapping |
| Unhandled error | 500 safe envelope | Full trace only in secured logs |

~~~python
from fastapi import Request
from fastapi.responses import JSONResponse

class ResourceNotFound(Exception):
    pass

@app.exception_handler(ResourceNotFound)
async def not_found(request: Request, exc: ResourceNotFound):
    return JSONResponse(status_code=404, content={"code": "resource_not_found", "detail": "Resource not found"})
~~~

Centralize mapping and protect logs; never expose vendor exception string or sensitive upstream URL in public body. Treat request id as a traceability hint not a security token.

## Critical tests
Create valid/invalid, unknown enum, extra fields, PATCH {} unchanged, PATCH explicit null policy, ownership, repeated POST/idempotency, optimistic conflict, pagination boundaries, stable JSON under ORM changes.

Official: https://docs.pydantic.dev/latest/concepts/serialization/ and https://fastapi.tiangolo.com/tutorial/handling-errors/ .
