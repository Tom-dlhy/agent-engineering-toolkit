# Python design: typing, model boundaries, errors and clean code

**Read when:** implementing type-safe business modules, DTOs, abstraction boundaries or quality reviews.

## Pick the right shape
- Frozen dataclass: domain value object and in-memory invariants; not automatic JSON validation.
- Pydantic model: untrusted transport/config serialization and validation; not a replacement for all domain objects.
- TypedDict: static typing of external dictionary payloads; not runtime checking.
- Protocol: meaningful behavior-boundary with multiple implementations or test fakes; not obligatory for every utility.
- Enum: finite public values; document compatibility when values change.

~~~python
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True, slots=True)
class Money:
    minor_units: int
    currency: str

class ResourceRepository(Protocol):
    async def get(self, resource_id: str) -> Money | None: ...
~~~

Use explicit domain names; avoid deep reliance on `Any`, magical decorators, mutable default arguments, import-time HTTP calls, module globals containing request state or hidden database access.

## Exception policy
Infrastructure adapter catches precise SDK/driver errors and maps to application exceptions. Service raises domain conflicts from invariants. API adapter returns public status and a stable safe error schema. Preserve exception chaining but do not surface raw error messages containing URLs, credentials or PII. Catch cancellation separately; avoid a blanket `except Exception: pass`.

## Review questions
- What exact invariant is checked, and in what layer?
- Can a caller accidentally create an invalid object?
- Does the function have unexpected side effects?
- Is API public DTO identical to DB model by convenience rather than design?
- Are error names/log fields stable across refactors?
- Do tests exercise negative cases and dependency failures?
- Are type checker suppressions narrowly justified?

Official: https://docs.python.org/3/library/typing.html , https://docs.python.org/3/library/dataclasses.html , https://docs.pydantic.dev/latest/concepts/models/ .
