# Roadmap

## Current state

- 148 first-party skills across 12 domains, with light / standard / deep workflows independent of skill knowledge depth.
- The AWS split, 35 UI provider branches and design/growth/refined methodology work use selective references.
- Additional skills remain condensed methodological overviews and are scheduled for deeper technical coverage.
- Read-only catalog discovery, path-safe individual reference reads, secure opt-in installations and deterministic CI checks.
- No imported third-party executable content, no self-updating prompts, no automatic merges.

## Priority: become operational experts

1. Backend and data: real FastAPI/Pydantic/SQLAlchemy/Alembic patterns, PostgreSQL transactions/performance, migrations and negative integration tests.
2. Frontend/frameworks: React/Next/TanStack app architectures; split Vue and Svelte; actual SSR and browser validation.
3. AI/agents: separate provider APIs, tool safety, evaluation and RAG from overly broad umbrella descriptions.
4. Cloud remainder: GCP/Azure/Cloudflare specialized paths, deployment/operations, IAM/network, Terraform and SRE depth.
5. Design/growth: verify motion and UI recommendations on real apps, test claims about search visibility against repeatable query sets; improve version-pinned examples.

## Planned: external Skill Package Manager

- Read-only search/inspect first, exact immutable SHA, license/NOTICE and dependency audit.
- Detect duplicates and overlapping triggers before creating new skills.
- Review scripts/network/credentials and sandbox tests; never execute during initial inspection.
- Propose source updates as reviewed diffs; no automatic installation or merging.

## Planned: behavioral evaluation

- Baseline vs toolkit scenarios for correctness, latency, selection, negative triggers and operator fixes.
- Measure exact tokens only when surfaced by host, otherwise label chars/4 as proxy.
- Keep costly model-driven evals manually invoked with explicit budgets and reproducible fixtures.

External sources and decisions: [V2 design and growth intake](design-growth-source-review.md).

## Completed partial Python vertical refactor
Python 3.x packaging, architecture, FastAPI, HTTPX, SQLAlchemy, observability and AWS/GCP/Azure LLM access now have indexed deep references. Remaining: build and execute concrete sample apps for each cloud provider, performance/chaos benchmarks, async DB contract suites, model eval dataset harness and version-pinned SDK compatibility CI. Do not infer fully production-tested implementations from Markdown static validation.

## Quality category refactor

Seven Quality skills have 21 task-scoped references and a source-driven audit;
deterministic routing/integrity tests and a local negative-test fixture were
added. Next evidence improvements: target-language E2E suites against real
apps, approved staging k6 profiles, security/ASVS review rehearsal, SLSA
attestation verification on actual artifacts, and independent agent
behavioral evaluation with held-out tasks. No skill maturity tiers.

## Architecture category complete as a source-reviewed content refactor

Eight architecture skills now have 24 targeted leaves and
a research audit. Automated tests can reject specific bad imports
and detect routing/reference regressions. Outstanding proof:
held-out agent design exercises, real DB outbox/saga fault
injection, toolchain/versioned OpenAPI client compatibility
and load/deployment measurements for concrete apps. The
toolkit does not proclaim architecture production-ready solely
from green static CI.

## Backend refactor — implemented, validation evidence still evolving

Seven Backend skills now expose 33 targeted references, including
modern Python, FastAPI, outbound HTTPX, SQLAlchemy, OpenTelemetry,
Celery and Node/TypeScript. A TypeScript HTTP test fixture runs
under Node 24, alongside existing Python FastAPI tests. Remaining:
strict Node/TS project compilation against a pinned tsconfig,
real Postgres concurrency/rollback suites, live broker crash tests,
authorized provider HTTP quota/fallback integration, SSE/proxy
load, tracing exporter, and held-out agent behavioral evaluations.
No maturity tiers and no blanket claim of proven production readiness.

## Data refactor — targeted expertise and verifiable SQL contracts

Data now has seven independent skills and 22 leaves. Primary
sources cover PostgreSQL planner/RLS, dbt incremental, GX 1.x,
Airflow 3.x, Snowflake Dynamic Tables, BigQuery billing,
Iceberg evolution, Debezium WAL and Flink checkpoint guarantees.
CI runs disposable Postgres integration RLS/constraint/rollback
tests and deterministic in-memory source revision replay tests.
Outstanding domain evidence: real DB online backfill with locks,
dbt/GX adapter runtimes, Snowflake/BigQuery costs/quotas,
multi-engine Iceberg/catalog writer tests, Debezium recovery,
Flink source-to-sink replay and real-agent held-out scenarios.
No blanket production/SOTA certification from static markdown.

## AI category refactor — source-verified, integration proofs still needed

AI includes eight skills, 26 reference leaves and three new task-scoped
specialists: durable agent orchestration, RAG engineering and MCP
2026-07-28 protocol implementation. Deterministic tool-executor policy
and query-time RAG tenant filter tests run offline; eval/routing metadata
and context limits remain validated. Remaining real-world evidence:
provider-native paid tests, LangGraph checkpoint crash recovery,
MCP SDK v2 server/client interop, retrieval index/ACL benchmarks,
model evals with consented datasets and supervised red-team.
No universal production/SOTA guarantee from green CI.

## Cloud provider-specific connectivity and operational gaps

Cloud category now provides per-service SDK/IAM/recovery guides
for AWS/GCP/Azure/Cloudflare, 41 specialists and 82 leaves,
with three new provider/edge opt-in profiles. Tests check
routing, safe reference access, Python syntax and discovery
budgets. The next evidence stage must validate live identity
and secret-free SDK reads in **authorized sandbox projects**,
regional quotas and pricing, network/private endpoints and
integration resilience (retry, redelivery, failover). Uncovered
services to evaluate individually: AWS SNS/KMS/Step Functions,
GCP Cloud Tasks/Eventarc/Firestore, Azure Cosmos/Event Grid/SQL,
Cloudflare KV/Queues/Durable Objects/Workflows and provider-specific
managed Kubernetes EKS/GKE/AKS and monitoring dashboards.
Avoid mass-importing a generic cloud services inventory.

## Frontend category refactor — source-verified implementation guidance

Seven frontend specialists with 21 references and an 18-skill optional discovery profile. A framework-neutral Node test fixture covers SSR serialization and direct API authorization. Future proof requires pinned React/Next/TanStack/Nuxt/SvelteKit/Angular/Astro project builds, Playwright browser hydration and security cases, web performance measurement and held-out agent activation evaluation. React Router full-stack specialist remains an individually assessed future candidate. Next proposed domain refactor: UI libraries.

## UI refactor — library correctness and distinctive product visual craft

All 35 existing providers were enriched in place and eight critical
vendor integrations were deepened (shadcn/Base/Chakra/HeroUI/MUI/
PrimeVue/Bits/Skeleton). The UI shared specialist now has five leaves;
frontend-design has three with product brief and anti-template review.
No catalog/profiles were added. Next evidence stage is actual
version-pinned provider projects, real browser/native screen captures,
keyboard/ARIA checks and task-based visual critique, not arbitrary
'AI-slop scores'.

## Design refactor — task-scoped visual engineering

Design retains 12 existing skills, with no new categories or style imports.
Six prior condensed skills now include 11 task-scoped references for WCAG 2.2,
accessible forms, theme SSR/contrast, responsive screenshot discipline,
truthful conversion design and opt-in bento/glass techniques. The broad
`ui-ux-design` profile no longer auto-installs niche bento/glass effects;
users can still install them explicitly. See
[design refactor decisions](design-refactor-audit.md). The next evidence stage
requires held-out real-agent routing, actual browser and assistive-tech journeys,
and measured context consumption; static tests cannot establish visual
originality, WCAG conformance or conversion gains.

## Design product UX expansion — provider-neutral decisions

Four distinct specialists extend the Design domain: interaction-flow-design,
information-architecture, content-design and data-visualization-design.
The visualization skill chooses truthful, accessible encodings while the
installed shadcn/Recharts, MUI X or other selected UI/provider owns actual
component APIs and rendering. No automatic chart library addition or parallel
visualization framework. General profiles gain only the applicable flow,
navigation and microcopy guidance; visualization is opt-in by individual skill.
See [Design product skills](design-product-skills.md) for boundaries and held-out
agent/browser verification backlog. This is a content/CI refactor, not yet an
observed improvement in user research or chart usability.
