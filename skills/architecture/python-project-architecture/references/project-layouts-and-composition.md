# Python project trees, composition root and ownership

**Read when:** scaffolding or refactoring package layout and dependency injection.

## Layered starter (small-medium service)

~~~text
app/
  main.py                # ASGI construction and lifespan
  api/
    resources.py         # HTTP semantics + request/response DTO
    dependencies.py      # transport DI bindings
  application/
    resource_service.py  # use cases + domain coordination
  domain/
    resource.py          # rules and invariants (if warranted)
    errors.py
  infrastructure/
    external_api.py      # HTTPX client, mapping errors
    repository.py        # SQLAlchemy adapter
  core/
    settings.py
    logging.py
    context.py
tests/
  unit/
  integration/
  contract/
pyproject.toml
uv.lock
~~~

More useful than placing every data shape in an unqualified models.py: distinguish HTTP request/update/response DTO from ORM table mapping and domain entity.

## Feature-first when product grows

~~~text
app/
  platform/              # configuration, telemetry, shared infrastructure
  modules/
    customers/
      api.py
      application.py
      domain.py
      persistence.py
    orders/
      api.py
      application.py
      domain.py
      persistence.py
  main.py
~~~

Avoid cross-module imports into internal tables; communicate through documented application interfaces/events and shared public contracts. The module boundary can enforce tenant isolation and transaction boundaries.

## DI composition
The application layer gets a Protocol or concrete typed collaborator; framework-only `Request` and `HTTPException` remain in the API adapter. App startup creates shared HTTP clients/engines; request dependencies create request-scope services/DB sessions. Test fakes implement behavior, not the entire SDK.

~~~python
from typing import Protocol

class ResourceReader(Protocol):
    async def get(self, resource_id: int) -> str | None: ...

class ResourceService:
    def __init__(self, reader: ResourceReader) -> None:
        self._reader = reader

    async def get_name(self, resource_id: int) -> str:
        name = await self._reader.get(resource_id)
        if name is None:
            raise ResourceNotFound(resource_id)
        return name
~~~

`ResourceNotFound` is a domain/application exception defined elsewhere. Avoid import-time client creation requiring env secrets; wire via lifespan at app construction.

## Failure boundaries
API maps 400/404/409/422/429/503 deliberately. Infrastructure converts known provider errors into meaningful internal outcomes (e.g., upstream NotFound ≠ always unavailable). Application decisions never inspect provider SDK exception class directly.

## Done
Diagram or tree with allowed import direction; request-scope and process-scope resources identified; integration and test boundaries mapped; no empty layers added for their names alone.

Official references: https://fastapi.tiangolo.com/tutorial/dependencies/ and https://docs.python.org/3/library/typing.html .
