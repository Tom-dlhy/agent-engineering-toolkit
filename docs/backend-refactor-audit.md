# Backend category — source-verified production engineering refactor

Research snapshot: 2026-10-11. Scope: **seven existing Backend skills**.
Charter: user-provided Agent Engineering Toolkit — Charte de gouvernance
et d'évolution (v2), emphasizing reuse before creation, independent
trigger, practical expertise and selective context reading.
Built from main after merged Core, Quality and Architecture refactors.

## Audit and actions

| Skill | Existing state | Refactor decision |
|---|---|---|
| modern-python | Four focused Python leaves, but missing CLI/batch and reproducible runtime | EXTEND, add two targeted leaves |
| fastapi-service | Four deep leaves, missing secure public API and stream backpressure | EXTEND, add two targeted leaves |
| python-http-clients | Three HTTPX leaves, missing outbound SSRF and total deadline | EXTEND, add two targeted leaves |
| python-persistence | Three SQLAlchemy leaves, limited async-session race and pooling detail | EXTEND, add two targeted leaves |
| python-observability | Two leaves, limited distributed baggage/cardinality | EXTEND, add one targeted leaf |
| background-jobs | Two leaves, Celery worker-loss nuance underspecified | EXTEND, add two targeted leaves |
| typescript-api | ~1 KB basic checklist, **no local references** | EXTEND, add four production Node/TS leaves |

No new skill needed: the seven are independently triggered. We keep the
interface with architecture (DDD/ports/API contract), quality (test strategy,
secure review), AI (LLM provider execution), data (database design) and cloud
(infrastructure) instead of duplicating them.

**15 new locally authored deep references, 18 existing retained = 33
Backend leaves**. All have the same single quality standard; the reference
count here reflects distinct responsibilities, **not** maturity rankings.
The seven SKILL.md entrypoints remain concise with selective routing.

## Primary-source verification

All important factual decisions compared against official references:

| Area | Official documentation | Specific decision |
|---|---|---|
| Python runtime and deployment | https://docs.astral.sh/uv/concepts/projects/sync/ and https://docs.astral.sh/uv/guides/integration/docker/ | --locked checks lock freshness; --frozen doesn't; runtime images/builds need target compatibility |
| Python typing and asyncio | https://docs.python.org/3/library/asyncio-task.html and https://docs.python.org/3/library/typing.html | Types are static hints; structured cancellation differs from CPU work |
| Pydantic Settings | https://pydantic.dev/docs/validation/2.12/concepts/pydantic_settings/ | Env naming, nested sources and secret precedence depend on exact config |
| FastAPI lifespan/security | https://fastapi.tiangolo.com/advanced/events/ and https://fastapi.tiangolo.com/tutorial/security/ | Lifespan controls shared resources; authN does not replace object authZ |
| HTTPX | https://www.python-httpx.org/advanced/timeouts/ and https://www.python-httpx.org/advanced/resource-limits/ | Connect/read/write/pool inactivity timeouts; overall deadline/retry budget is separate |
| SQLAlchemy | https://docs.sqlalchemy.org/en/20/orm/session_basics.html and https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html | Mutable AsyncSession cannot be shared across concurrent tasks; explicit loading avoids implicit async I/O |
| Alembic | https://alembic.sqlalchemy.org/en/latest/autogenerate.html | Autogeneration is a candidate migration to review, not automatic deploy proof |
| OpenTelemetry | https://opentelemetry.io/docs/languages/python/instrumentation/ and https://www.w3.org/TR/baggage/ | Trace/correlation isn't an auth identity; propagating PII in baggage is unsafe |
| Celery | https://docs.celeryq.dev/en/stable/userguide/tasks.html | acks_late and retry are distinct; worker loss may ACK even with acks_late |
| Node.js and TypeScript | https://nodejs.org/api/typescript.html and https://nodejs.org/api/test.html and https://www.typescriptlang.org/tsconfig/strict.html | Native type stripping and runtime tests do not replace static tsc |
| Fastify | https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/ | Ajv/schema validation and serialization; untrusted schemas should not be compiled |

Stack Overflow can reveal reproducible edge cases and diagnostics, but
changes to semantics, security, runtime and SDK APIs use primary sources.
SOTA means current, version-aware and adaptable to workload, not one
"best framework" or universal users-per-worker threshold.

## Executable artifacts and QA evidence

- Existing FastAPI example with 11 HTTPX MockTransport integration tests
  remains, with documented missing production authentication/persistence.
- New educational **TypeScript Node API fixture** in examples/backend-typescript
  uses native Node test runner with injected identity, runtime validation,
  tenant isolation, replay/idempotency and safe HTTP error mapping.
  Runs on pinned Node 24 in CI; **runtime execution is not tsc typechecking**.
- Backend routing scenarios cover seven positive, seven negative
  neighboring, unmatched cases, path traversal and context budgets.
- Entire global Python unittest suite, FastAPI tests, 113 skills and 16
  profiles validated by existing CI.

## Gaps intentionally not claimed as complete

There is no real PostgreSQL concurrency/transaction-integration deployment,
no full production OTel exporter, no load-tested WebSocket/SSE proxy,
no live Celery broker worker crash suite, no real Node auth provider/DB,
and no end-to-end AWS/GCP/Azure LLM calls in this PR. A green CI
does not prove those behaviors or an agent's architecture choice
on unseen tasks. Those require authorized integration resources,
load tests and held-out agent evaluations. No external code imported.
