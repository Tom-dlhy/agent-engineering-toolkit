# Hexagonal ports/adapters — adoption and import enforcement

**Read when:** deciding whether decoupling is worthwhile,
converting a tightly coupled Python service or enforcing
dependency direction with executable checks.

## Is a port justified?

| Situation | Starting point |
|---|---|
| Single stable HTTP SDK call in short script | Typed concrete adapter, no ceremony |
| Complex rule plus external HTTP/DB side effect | Extract application function and dependency |
| Several providers implementing same business capability | Protocol/port with explicit capability variants |
| Domain aggregate independent of web/ORM | Inward domain/application dependency direction |
| Vendor streaming/tools differ fundamentally | Capability-specific ports, no fake common subset |

One interface for each private helper increases boilerplate without
improving testability; "ports" belong at behavior/change seams.
Use concrete adapters behind a Protocol only when it serves a
real contract, replacement/testing or domain isolation.

## Python import rule

~~~text
domain      → Python stdlib and domain-only dependencies
application → domain + declared ports
adapters    → application/domain + external SDK/ORM
composition → constructs adapters and injects app services
transport   → application + transport framework
~~~

Domain must not import FastAPI, SQLAlchemy model, HTTPX or LLM
provider SDK. The composition root may know about each layer.
A single-layer prototype can still have coherent side effects
without physically creating five empty packages.

## Enforcement test (concept)

Scan AST import/import-from of relevant packages, map resolved
module names and reject domain→infrastructure imports.
Use import-linter or custom stdlib test, but handle relative
imports and package aliases accurately. Avoid false reassurance
from regex grep or tests that never introduce a failing case.

## Migration

Pick one fragile boundary; preserve HTTP/DB behavior with
characterization tests, introduce behavior port, move vendor
code behind adapter, wire lifespan dependency, run real
contract test, then enforce import rule. Don't rewrite all
services at once because a folder convention looks appealing.

## Evidence

Unit use case tests with fake port, integration tests with
actual DB/SDK in authorized sandbox, error/status translation,
resource close/cancellation and forbidden-import fixture.

Sources:
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html and
https://docs.python.org/3/library/typing.html .
