# Roadmap

## Current state

- 178 first-party skills across 14 domains (13 technical + 1 optional behavioral-persona domain), with light / standard / deep workflows independent of skill knowledge depth.
- The original 12 technical domains underwent source-reviewed refactors (through merged PR #25); 15 independent self-contained personas are available opt-in in their own opt-in domain. The catalog retains **423 technical reference leaves** and **20 installation profiles**.
- The AWS split, 35 UI provider branches and Design/Growth/Stacks selection skills use targeted references. Practical depth and real-world integration evidence still vary by skill.
- Read-only catalog discovery, path-safe individual reference reads, secure opt-in installations and deterministic CI checks.
- No imported third-party executable content, no self-updating prompts, no automatic merges.

## Adaptive engineering methodology — implemented, real-agent proof pending

The optional implementation-planning Core skill now provides task/interface
contracts and three selective reference leaves. Existing task-routing,
verification-before-done, git-pr-workflow, execution-orchestrator and
review-feedback-arbiter own risk-based workflow, R0/R1/R2 review, inline/
delegated/parallel execution, safe worktrees, branch finalization and review
feedback. The toolkit.adaptive_policy module is a deterministic **advisory**
on structured observations; test cases cover low-risk edits, one-line
authorization risk, missing reviewer/approval and parallel-isolation refusals.
Three engineering profiles opt into planning; minimal and fullstack retain
their original inventory. No additional persona is created.

Known limits: static CI does not prove Codex/Claude runtime activation,
the actual number of model tokens saved, or behavioral parity with Superpowers.
Run consented held-out A/B tasks with agent logs and measurable correctness,
latency and human correction before such claims. See
[adaptive methodology](adaptive-engineering-methodology.md).

## Research-driven operational deepening (2026-10-12)

Fourteen existing skills across six priority sectors were expanded in place,
with eight already-registered expert reference leaves deepened. The
source-pinned audit and scope decisions are in
[methodology source review](methodology-source-review-2026-10.md).
Twenty held-out cases in evals/methodology-depth.yaml are **unexecuted**;
tests/test_methodology_depth.py checks their structure and the existence
of the methods. scripts/summarize_skill_evals.py only aggregates
externally observed, comparable old-skill/new-skill records and refuses
to invent missing token data. Behavioral quality, actual activation and
measured token savings remain open until native tests are authorized/run.

## Next priorities — validate behavior, not grow the catalog

1. **Discovery/routing:** address the observed lexical router's weak handling of natural French queries, synonyms and ambiguous tokens (for example `base` matching `base-ui` for a database-selection question). Benchmark positive, negative and multi-domain routing before considering a more complex retrieval system. **This is a separate code change; it is not fixed by documentation updates.**
2. **Held-out agent evaluations:** compare the same real engineering tasks with and without toolkit skills; measure correct activation, unnecessary loading, task completion, introduced defects, human corrections, latency and actual tokens where available. Current `evals/*.yaml` are mostly **unexecuted scenario specifications**, not success results.
3. **Real integrations:** use authorized version-pinned apps to validate frontend SSR/keyboard/assistive technology, API and cloud SDK behavior, database migrations/restore, identity boundaries and safe deployment paths. Differentiate passing offline fixtures from working production stacks.
4. **Claims and maintenance:** recheck version-sensitive official docs, hosting limits, feature entitlements and legal requirements before use; capture test provenance and update only the skills whose real failures justify changes.

## Installer v2 — opt-in implementation, live host acceptance pending

Managed local installation, persistent ownership ledger, cumulative profiles,
SHA drift checks, read-only doctor, update/repair/uninstall, journal recovery,
release metadata and native Codex/Claude plugin packaging are implemented.
Cross-platform lifecycle suites run in CI; real agent activation (including
negative routing and measured outcomes) remains a separate acceptance gate.
See [Installer v2](installer-v2.md).

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

Seven Quality skills have 24 task-scoped references and a source-driven audit;
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

## Growth operational refactor — source-reviewed and provider-neutral

The existing SEO, content and AI-search specialists were deepened with six
new targeted leaves (four leaves each). Two independent opt-in growth skills
cover controlled experimentation and permissioned lifecycle/retention journeys
with three additional leaves each (18 Growth leaves total). No marketing
platform, tracking SDK or email service was installed; providers and legal
requirements remain project-specific. See [Growth refactor audit](growth-refactor-audit.md).
Deterministic fixture tests enforce selected event/assignment and suppression
invariants but **do not** establish real campaign or experiment outcomes.
Stacks was subsequently completed in merged [PR #25](https://github.com/Tom-dlhy/agent-engineering-toolkit/pull/25). The next phase is held-out agent evaluation and authorized real browser/crawler/provider checks; no observed ranking, conversion or message-delivery outcome is asserted here.

## Stacks final domain refactor — composable selection

Existing `stack-advisor`, `database-selection`, `ui-library-selection`
are extended in place. One **independent** new `authentication-solution-selection`
specialist addresses user identity provider choice, federation and session
risk—not cloud IAM or provider SDKs. Four Stacks skills have 12 targeted
local reference leaves (11 new, original UI library map retained).
No ORM/framework/hosting-by-vendor micro-skills, installation profile growth,
automated dependency installs or production migrations. See
[Stacks governance audit](stacks-refactor-audit.md).

All 12 categories have now undergone domain-level source review, but this is
**not** proof of production-quality behavior. Next: cross-category held-out
agent evaluation and authorized real-project integration, browser, provider
and security review, documenting where routed skills actually help or collide.

## Persona operating protocols — proposed new optional domain

Fifteen self-contained behavioral protocols (the original twelve plus engineering leadership,
privacy compliance coordination and cross-media brand/creative direction) are authored
in `skills/personas/`.
Their independent triggers and exclusions deliberately avoid replacing the
existing core/quality skills or `agents/*.md` briefs. No references folder or
external documentation is necessary for their operation, and none is added
to default profiles. See [persona governance and evaluation](persona-protocols.md).
The original 12 technical categories are not modified by this persona-focused
addition. Held-out conversational agent tests and real host installation
remain **future evidence**, not completed validation.

## Additional opt-in personas — engineering, privacy and branding

Three new independent operating modes follow merged PR #27:
`head-of-engineering` guides engineering organization, capacity and
quality policy across initiatives; `privacy-compliance-lead` maps
processing purposes, privacy risk, rights and approval gates without
claiming legal certification; `branding-lead` art-directs identity and
cross-channel campaigns, including promotional-video storyboards and
creative QA. Technical design skills still own logo boards, UI motion,
component tokens and production APIs. The proposed catalog holds
**166 skills / 13 domains** (historical persona-stage snapshot), with **15 opt-in persona methods** and
unchanged **382 technical references / 20 profiles**. No live creative
asset or compliance audit is claimed; held-out behavior tests remain
unexecuted.

## Snowflake platform experts — proposed expansion (2026-10-12)

Five source-reviewed operational Snowflake specialists are proposed in a
new `data-platforms` technical domain (Query Performance, Data Pipelines,
Snowpark ML, Cortex AI, Security/Governance). This is a distinct set of
platform API and operational skills, not a Snowflake vendor rewrite of
`lakehouse-engineering`, `data-pipeline-quality`, `analytics-modeling`
or `llm-evaluation`. Each has three deep local reference leaves: the
proposed catalog has **177 skills / 14 domains / 415 references / 20 profiles**.
These are authored examples plus deterministic routing tests, **not**
production Snowflake integration or paid warehouse benchmarks. Follow-on
Databricks/BigQuery/Fabric/Redshift must be individually re-audited for
unique utility before creation. Source review: [Snowflake audit](snowflake-platform-audit.md).

## Databricks specialists — proposed 2026-10-12

Six independent provider specialists extend the existing data-platforms domain
with Spark/Delta, Lakeflow, Unity Catalog, MLflow MLOps, Declarative Automation
Bundles and Unity Gateway AI governance. Current catalog proposal: **177 skills,
14 domains, 415 reference leaves, 20 profiles**. Source and non-duplication
audit: [Databricks platform](databricks-platform-audit.md). Existing Snowflake
skills and Data/AI/Cloud expert ownership remain unchanged. Tests here are
local deterministic and textual; real Databricks workspace, DBU benchmarking,
managed service access, production policy enforcement and held-out agent
behavior are **not** verified. Avoid auto-expanding the catalog to other providers.
