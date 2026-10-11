# Skill depth audit — phased history and current backlog

## Phase 1 historical baseline (2026-10-11)

The inherited `feat/modular-skill-engine` branch has **59 first-party skills**, approximately **1.1 KiB/skill on average**, with **zero local reference files or examples**. This is a capable routing foundation, **not** a technically exhaustive skill library. At this historical phase-1 snapshot, UI [PR #9](https://github.com/Tom-dlhy/agent-engineering-toolkit/pull/9) was still open; it has since merged into main.

Phase 1 keeps the original 59 entries, refactors the broad `aws-integration` skill into a cross-service coordinator, and adds six independently activated service skills. Therefore at the phase-1 snapshot the branch contained **65 catalog entries**, with seven AWS specialist skills having substantial references at that snapshot. That snapshot did **not** claim all 65 met the final standard. Later phases are recorded below.

## Audit verdict by domain

| Existing domain | Finding | Recommended evolution |
|---|---|---|
| core (4) | Small methodological procedures; depth can be proportional | Keep focused; add routing and negative-trigger evaluations |
| architecture (7) | Method and patterns are mostly one-screen summaries | Deep references for transactions, architecture boundaries, ADR examples and migrations; no duplicate DDD/hexagonal skills |
| backend (4) | FastAPI, modern Python, TypeScript and workers lack implementation playbooks | Prioritize FastAPI/Pydantic/async/auth/SQLAlchemy and Python packaging; consider splitting Node frameworks only if triggers and methods differ |
| cloud (12 before phase 1) | AWS/GCP/Azure umbrella skills each bundle many unrelated services | **Split AWS first**; then evaluate GCP Cloud Run/PubSub/IAM/Vertex and Azure Functions/Storage/identity independently; enrich Terraform/Cloudflare/Kubernetes |
| data (4) | Database, migrations and Postgres performance already have distinct responsibilities but little depth | EXTEND and add deep query/migration examples instead of splitting by every table |
| AI (4) | LLM, RAG and tools governance overlap yet contain very little practical detail | Define output contracts, eval harness, provider-specific adapters and retrieval failure modes; separate true provider APIs only where independent |
| design (11) | Skill scopes often overlap (frontend, landing, grids, typography) | Consolidate aesthetic decision rules where appropriate, keep precise specialized techniques as references, add visual QA examples |
| frontend (4) | `vue-svelte-patterns` combines two unrelated frameworks | Candidate for **SPLIT** into Vue and Svelte skills; React/Next/TanStack deserve framework-specific implementation guides |
| quality (7) | Operational checklists are adequate starting points, not deep testing/security guides | Enrich testing strategies, security review payloads, reproducible code checks and measurable criteria |
| stacks (3) | Decision-only skills, reasonable to keep compact | Strengthen decision matrices, actual framework compatibility and cost/risk evidence |

## Uniform definition of an acceptable skill

- Narrow, uniquely activated scope with an explicit exclusion.
- A `SKILL.md` **capable of deciding**, not merely linking to documentation.
- Real, locally present targeted leaves **as needed by its responsibility**, with explicitly differentiated read conditions.
- Leaves contain specific mechanisms, runnable/adaptable examples, failure modes and negative tests, not just general advice.
- Version-sensitive claims refer to official vendor docs; current deployment/model support still must be checked.
- Static validation checks presence/index/path safety, never treats bytes alone as expertise.
- Routing tests show one positive, one negative and ambiguity across sibling skills.
- Context test proves metadata remains within profile budgets while leaf contents are omitted until explicitly chosen.

## Phase roadmap

1. **This PR (AWS vertical slice):** 1 coordinator + 6 specialist skills; 14 deep references; safe targeted CLI reading; link validation; tests and context audit.
2. **Backend and data:** FastAPI and Python async/auth/SQL migration references; PostgreSQL, schema migrations; evaluate split of TypeScript web frameworks.
3. **Frontend and design:** Vue/Svelte split with independent examples, React/TanStack/Next deep manuals; integrate or reconcile UI PR #9 *after* base branch merges, avoiding overlapping registry/profile changes.
4. **AI:** LLM integration, provider-specific Bedrock/OpenAI/Anthropic tradeoffs, tool safety, eval reliability, RAG evaluation.
5. **Cloud rest + quality:** GCP/Azure service-based splits, Cloudflare D1/R2/Access, Terraform/K8s, security, SRE, CI/CD, release and tests.
6. **Global review:** consolidate duplicate knowledge, benchmark skill selection/reference reads in actual Codex and Claude, measure actual token usage where host surfaces it.

Review each refactor on its own merits; no mass-generated placeholders or skill maturity badges. All skills require the same acceptance contract, and structural CI alone cannot prove applied expertise.

## Phase 2 historical snapshot — UI integration (PR #9)

The original PR #9 is now reconciled with main after PR #5 and PR #10 merged. At the phase-2 snapshot, the repository contained **101 unique skills**, including **35 opt-in UI library providers**, one shared `ui-component-research` and exactly one `ui-library-selection` under `skills/stacks`. UI-specific references: **70 local provider leaves + 4 shared component-family leaves + 1 selector map**. Existing seven AWS specialists retain their references.

The 35 UI providers have version-checking implementation and integration playbooks, but static validation is not evidence that every vendor API, full production workflow or accessibility behavior was tested against a live app. Some providers remain broad and need further version-pinned component examples and agent behavioral evaluation. Treat source citations as directions for freshness, not permission to assume current props.

Follow-up work: run representative benchmark apps for web, Vue/Angular/Svelte, React Native and Flutter, test a form/overlay/data table from each selected provider under the installed release, measure skill-selection errors, and close specific capability gaps after review. Do not force all 35 into standard install profiles.

## Phase 3 — curated design craft and Growth (PR #11)

Current PR #11 increases the catalog to **106 unique skills across 12 domains** by introducing five independently activated skills: `core/requirements-discovery`, `design/brand-identity-visualization`, and `growth/content-strategy`, `growth/technical-seo`, `growth/ai-search-visibility`. Six existing skills are extended rather than duplicated: `interaction-motion`, `frontend-design`, `ux-audit`, `design-system`, `typography-layout` and `external-skill-audit`.

A total of **24 new local reference leaves** were authored with narrow read conditions. The 11 affected skills follow the same acceptance contract as the rest of the catalog; actual browser/runtime tests and behavioral evaluations remain necessary. The AWS and UI specialists remain intact. All external source decisions and immutable revisions are documented in [source review](design-growth-source-review.md); scripts, hooks and datasets were not copied.

**Remaining coverage gaps:** backend and databases still lack deep references; GCP/Azure/Cloudflare specialization, full framework coverage and rigorous evaluation remain future phases. Documented SEO methods do not guarantee public indexing, rich results or AI-answer citations.

## Phase 4 — Python architecture + production LLM multi-provider integration

This branch starts from a merged 106-skill main and reaches **113 skills / 16 profiles**. It creates seven narrowly triggered specialists: `python-project-architecture`, `python-http-clients`, `python-persistence`, `python-observability`, `python-llm-gateways`, `gcp-vertex-ai`, `azure-ai-foundry`. It substantively rewrites `modern-python`, `fastapi-service`, `background-jobs`, `python-ddd`, `hexagonal-architecture` and `llm-integration` — not duplicated.

35 local leaves include typed Python/package/async/settings/architecture guidance, FastAPI/Pydantic/HTTPX, SQLAlchemy and transactions, JSON logs/OpenTelemetry, LLM contracts/production risk, LiteLLM/LangChain/LangGraph, GCP Google Gen AI, Microsoft Foundry and Python DDD/ports/jobs. The existing AWS Bedrock specialist is reused rather than recreated. All skills share the same acceptance contract; real integration and agent evaluations are required to verify behavior and model-version compatibility.

See [Python decision matrix](python-engineering-v2.md) and source notes. Static checks validate routing/leaf paths/context safety, **not** real credentials, production scaling, correctness of every vendor variant or cost/quality; examples require target-version verification.

## Phase 5 — Core category and unified skill-quality contract

All **five Core skills** were audited and refactored in place: task-routing, systematic-debugging, verification-before-done, skill-authoring and requirements-discovery. Four previously short skills gained **eight targeted procedural leaves**; requirements-discovery retains its two substantial leaves with clearer activation boundaries. No new skill was registered.

The registry's **66 historical maturity fields were removed** without adding replacement tiers or ranks. All reference paths declared by any skill now receive the same structural safety validation; no arbitrary two-leaf minimum is imposed on methodological skills. Exact-depth and behavioral evidence are still needed per technical domain before claiming individual task readiness. See [Core audit and test matrix](core-refactor-audit.md).

## Phase 6 — Quality category and verified technical methods

Seven pre-existing Quality skills were refactored **without creating another
registered skill**. Six short methodological entries now have three deep,
task-directed local references; the existing external-skill-audit gained an
adversarial-evaluation leaf. This contributes **19 new leaves** and a total
of 21 indexed Quality references. See [Quality refactor audit](quality-refactor-audit.md).

Methods and claims were compared against primary official sources including
pytest, OWASP ASVS 5.0.x, NIST SSDF final 1.1, GitHub Actions/rulesets,
SLSA 1.2, Python profiling and Grafana k6. The tests cover deterministic
discovery/negative routing, leaf access and a separate educational
authorization/idempotency fixture. Real penetration/load tests, provider
environments and agent behavioral evaluations remain unperformed.
Every skill continues to obey the same **uniform** quality contract; no
maturity ranks.

## Phase 7 — Architecture source-verified refactor

Eight existing Architecture skills were audited in place, with
**17 new detailed references** plus 7 retained leaves = 24 total.
API contract version/toolchain support, RFC 9110/RFC 9457,
modular monolith versus microservices, DDD contexts and hexagonal
ports, event delivery/outbox/saga, ADR and TCO decisions are
explicit and sourced. See [Architecture audit](architecture-refactor-audit.md).

A dependency-boundary CLI fixture and its negative tests, plus
lexical routing and reference tests, verify selected properties;
live deployment/concurrency/load and real-agent semantic selection
remain unverified. One quality standard, no per-skill ranks.

## Phase 8 — Backend Python and TypeScript source review

All **seven existing Backend skills** were upgraded without creating
new selectors. Fifteen new deep references bring the total to
**33 Backend leaves** (six Python-focused specialists and
TypeScript/Node). Documentation and decisions were reconciled with
FastAPI/Pydantic, uv, HTTPX, SQLAlchemy, OTel, Celery, Node,
TypeScript and Fastify **official** references. Negative
routing and a native Node 24 TypeScript runtime test demonstrate
specific behavior; they do not prove full typechecking,
real DB/broker/provider behavior or production scalability.
See [Backend research and test audit](backend-refactor-audit.md).

## Phase 9 — Data source-verified refactor (2026-10-11)

Four short Data skills were upgraded with 13 task-specific deep references.
Three new, non-overlapping skills were added: `analytics-modeling`
(business grain/dbt/fact-dimension), `lakehouse-engineering`
(Parquet/Iceberg/Snowflake/BigQuery storage and cost) and
`streaming-cdc-engineering` (Debezium/Flink WAL/event time/checkpoint).
**7 Data skills, 22 leaves; 116 catalog skills overall, 16 profiles.**
The data-engineering profile deliberately adds all three skills' compact
metadata while leaving full leaves opt-in. Real PostgreSQL 18 SQL/RLS
integration checks and a pure Python CDC replay fixture complement
lexical routing and reference safety. See
[Data audit](data-refactor-audit.md) for official sources and limits.
This is uniform quality, not a maturity rank.

## Phase 10 — AI domain and official-spec interoperability

Five existing AI skills were expanded and clarified, plus three
independent specialists for agent-orchestration, rag-engineering and
mcp-integration. **Eight AI skills and 26 selected references total**
(20 new, 6 retained); the catalog now holds 119 skills with
16 profiles. Specific facts cross-checked against MCP
2026-07-28, LangGraph, LiteLLM, OWASP, OpenAI, AWS and Vertex.
Offline authorization/RAG fixtures and negative lexical routing are
necessary but not proof of real model behavior. Consult the
[AI refactor research audit](ai-refactor-audit.md). No maturity ranks.

## Phase 11 — Cloud service-level connection and production semantics

Previous category state: 19 Cloud skills (9 deep service specialists
retained, 10 light/general skills needing improvement). The ten
cross-provider/coordination skills were extended with 20 technical
leaves and routing. **22 new independently triggered service skills**
were added across AWS (6), GCP (6), Azure (6) and Cloudflare (4),
with 44 further leaves. Cloud now has **41 skills / 82 local
references**; catalog contains **141 skills and 19 profiles**.
See [official-source Cloud audit](cloud-refactor-audit.md) and
[connection map](cloud-service-map.md). Static docs, fake tests and
routing checks do not demonstrate live permissions or deployment.
All have one uniform quality contract, never maturity rankings.

## Phase 12 — Frontend framework source review

React, Next.js, TanStack Start upgraded with three practical deep leaves each; the combined Vue/Svelte skill was replaced with Vue/Nuxt and Svelte/SvelteKit, and Angular/Astro added as independent domains. Seven frontend skills now expose **21 leaves**. Catalog **144 skills / 20 profiles**, preserving metadata-only discovery. See [Frontend audit](frontend-refactor-audit.md) and [framework map](frontend-framework-map.md). Browser/framework adapter integration remains a follow-up, not presumed by green structural CI.

## Phase 13 — UI library release gates and product-grounded visual quality

Refined 35 provider SKILL.md files, eight high-risk integration leaves,
ui-component-research (five leaves) and frontend-design (three leaves).
Official references include shadcn, Base, HeroUI, Chakra, MUI,
PrimeVue, Bits, Skeleton, W3C, Anthropic and Vercel. The toolkit still
has **144 skills / 20 profiles** without graded maturity levels.
No vendor sample was automatically installed. See
[UI refactor audit](ui-refactor-audit.md) and
[production visual rubric](ui-production-quality.md).
