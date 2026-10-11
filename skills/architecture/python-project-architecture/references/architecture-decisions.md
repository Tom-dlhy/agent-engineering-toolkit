# Python architecture decision guide

**Read when:** choosing initial structure or reviewing whether current Python architecture fits complexity.

## Complexity, not fashion
| Situation | Start with | Promote when |
|---|---|---|
| Disposable exploration | Script/functions | Reuse, secrets, deployment, tests require packaging |
| Small single-domain service | Feature folder or simple API/services/adapters | Business rules and integrations grow |
| Several features, one deploy | Modular monolith by bounded capability | Independently owned modules need contracts |
| Complex invariants, multiple adapters | DDD/hexagonal selectively | Need explicit consistency and behavior ports |
| Independently scaling domains | Services only with operational proof | Clear boundaries, team ownership and transactional design |

Layered structure is good until a `services/` folder holds 40 unrelated feature use cases. Feature-first layout is often easier to navigate as codebase grows. Hexagonal can still be in one deploy; microservices are not a prerequisite.

## Decision forces
Domain invariants; coupling between features; boundary stability; independent deployment; transaction scope; authorization model; change frequency; testing costs; observability and on-call ownership. Don't claim "clean architecture" by naming folders without import-dependency enforcement.

## When NOT to abstract
One external API, stable contract, two functions: a direct typed adapter may be fine. A generic repository interface mimicking all SQL operations can obscure business needs. Prefer deliberate composition and testable pure logic over inheritance hierarchies.

## Architecture Decision Record example
Context: CRUD API with external billing service, team 2, single database. Decision: layered single deploy with billing adapter and transaction boundary; no event bus. Revisit if billing becomes independent job with reliability requirements. Consequences: simple deployment, retry risk must be addressed separately.

## Testing boundaries
Unit tests for pure policy, adapters with fake HTTP, integration tests against actual DB, HTTP contract tests, one end-to-end transactional path. As domain complexity increases, add architectural import checks to prevent infrastructure imports inside domain.

Official background: https://fastapi.tiangolo.com/tutorial/bigger-applications/ and https://docs.python.org/3/library/typing.html .
