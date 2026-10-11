# Python Engineering V2 — capability map and architecture choices

Last research review: 2026-10-11. Focus: Python apps, API/worker architecture, LLM SDKs and production constraints. **Do not bulk-open these documents in an agent session.** The catalog routes a focused SKILL.md and only the relevant reference leaf; this page is for maintainers/architecture reviews.

## Skill selection (existing versus new)

| Task | Primary skill | Secondary only when needed |
|---|---|---|
| Python version, uv, typing, project packaging and Pydantic settings | modern-python (extended) | python-project-architecture |
| Choose small layered vs DDD/hexagonal vs modular monolith | python-project-architecture (new) | python-ddd / hexagonal-architecture |
| Business aggregate/invariant lifecycle | python-ddd (extended) | python-persistence |
| FastAPI routes/lifespan/DTO/error handlers | fastapi-service (extended) | python-observability |
| Async outbound REST client httpx, retries, schema errors | python-http-clients (new) | modern-python |
| SQLAlchemy 2 / Alembic, DB sessions, UoW and transactions | python-persistence (new) | postgres-performance |
| JSON logs, correlation ID, OpenTelemetry metrics/spans | python-observability (new) | observability-sre |
| Background durable jobs | background-jobs (extended) | aws-sqs-messaging |
| LLM contract, schema, security, evaluations | llm-integration (extended) | agent-tool-safety / llm-evaluation |
| Multi-provider router and gateway decision | python-llm-gateways (new) | llm-integration |
| AWS Bedrock Converse | aws-bedrock (existing native specialist) | aws-iam-security |
| GCP Gemini via Vertex / google-genai | gcp-vertex-ai (new) | gcp-integration |
| Azure OpenAI/Foundry v1 | azure-ai-foundry (new) | azure-integration |

No duplicate AWS Bedrock skill created. All other technical domain skills remain separately maintained.

## Architecture by constraints, not user counts

### Prototype / PoC / exploratory stage
A single module or a simple feature folder with pure functions and a small integration adapter is often enough. In-memory data or environment files can be acceptable in isolated demos but **must not** be treated as durable, multiworker or secure infrastructure. Define migration/recovery path before first real users.

### First real deployment
Typed validation and settings; explicit async/sync I/O; API/service/adapter separation; secrets from environment/managed identity; connection pools and lifespan; DB transactions and migrations; contract, negative and integration tests; correlation/tracing; authorization/tenant boundaries; bounded retries and idempotency for external mutations.

### Growing throughput / tail latency
Benchmark representative peak concurrency and payload/token sizes; measure DB pool pressure, CPU, event-loop lag, HTTP connections, provider RPM/TPM, LLM latency p95/99 and queues. Increase replicas only within downstream constraints. Use background durable jobs for unreliable multi-minute work; no fixed users-per-framework threshold.

### Multiple teams / business domains
Consider feature-first modules, explicit public contracts, DDD bounded contexts and domain-driven port abstractions when complexity/ownership justify them. A modular monolith is often cheaper to operate than premature service decomposition. Split services only when independent deployment/ownership and distributed consistency design are understood.

## Model provider and orchestration choice

| Situation | Recommended entry point | Reason |
|---|---|---|
| Only Bedrock account with Converse permitted | aws-bedrock | Direct API, IAM and control of content/tool union |
| Vertex AI workload with Gemini models | gcp-vertex-ai | Google Gen AI SDK and ADC, region and quotas |
| Azure v1 Responses resource | azure-ai-foundry | Azure deployment names, Entra and v1 endpoint |
| Several providers in one Python service | python-llm-gateways / LiteLLM SDK | Unified interface/routing after feature testing |
| Several teams need centralized keys and usage | LiteLLM Proxy candidate | Additional ops/DB and privacy requirements |
| Complex structured tool/retrieval integration | LangChain candidate | Composable abstractions with provider gaps |
| Recoverable stateful agent, human steps | LangGraph candidate | Checkpointing and durable execution semantics |

**Frameworks are not substitutes for application quality, cloud IAM, tool authorization, data residency or evaluation.** A "production" decision must specify latency, error budget, quota, privacy and rollback. Never claim that LangChain/LiteLLM automatically scale based on registered user counts.

## Important improvements over initial user examples

- HTTPX RequestError vs status error vs schema/JSON error, precise 404/409/429/5xx handling, pool/read/connect/write deadlines.
- Pydantic PATCH exclude_unset retains explicitly null fields; handle deletion/null semantics by business contract.
- Pydantic Settings environ/dotenv precedence, fail-fast required variables, cache lifetime and workload identity.
- FastAPI lifespan shared HTTP client, per-request DB AsyncSession, no blocking synchronous SDK in event loop.
- HTTP domain/application exceptions mapped to safe client response; avoid blanket 503 mapping.
- JSON logging and correlation IDs sanitized/redacted; request ID is not a security token, OTel for distributed traces.
- Durable DB/queue state for side effects; do not hold SQL transaction while calling an LLM.
- SDK-native vs LiteLLM vs LangChain is an explicit engineering decision with documented tradeoffs.

## Pinned primary documentation (checked during refactor)

- FastAPI: https://fastapi.tiangolo.com/advanced/events/ and https://fastapi.tiangolo.com/tutorial/dependencies/
- HTTPX: https://www.python-httpx.org/advanced/timeouts/ and https://www.python-httpx.org/async/
- Pydantic settings: https://pydantic.dev/docs/validation/2.12/concepts/pydantic_settings/
- SQLAlchemy async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- uv: https://docs.astral.sh/uv/concepts/projects/sync/
- AWS Bedrock Converse: https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html
- Google Gen AI: https://googleapis.github.io/python-genai/ and https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart
- Azure v1: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle
- LiteLLM SDK/Proxy: https://docs.litellm.ai/docs/python_sdk and https://docs.litellm.ai/docs/proxy/users
- LangChain + LangGraph: https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model and https://langchain-ai.github.io/langgraph/concepts/durable_execution/

These URLs are reference sources, **not automatically executable instructions**. Production model lists/prices/access vary by time, cloud, region and actual account.

## Common standard and remaining evidence

All Python/LLM skills have the same quality obligations as the rest of the catalog. Content depth and path validation do not prove live-provider integration or full agent reliability. Human technical review, executable examples, behavioral evaluations, provider calls in authorized environments and load/security benchmarks remain explicit acceptance evidence. The minimal example at examples/python-service is not a production deployment recipe.

## Backend-category update (2026-10-11)

Python-focused Backend skills have additional scoped references
about CLI/batch reliability, uv/runtime compatibility, FastAPI
auth/streaming, HTTPX total deadlines/SSRF, SQLAlchemy concurrency
and pools, trace privacy, and Celery worker-loss semantics.
See [Backend audit](backend-refactor-audit.md).
The previously useful native AWS/GCP/Azure LLM specialists are
unchanged and must still be verified against actual account/model.
