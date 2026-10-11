# Agent Engineering Toolkit

**Vendor-neutral AI engineering skills, workflows and quality gates — modular by design, economical in context.**

A growing library of **166 first-party skills across 13 domains**, with **20 small installation profiles**, lightweight `light / standard / deep` workflows, optional agent role briefs, and a **deterministic local skill finder**. Designed for Claude Code, Codex and other compatible environments without requiring an LLM API call to discover skills.

> Status (2026-10-12, following merged PR #27; three additional opt-in personas proposed): the original **12 technical domains** have undergone source-reviewed refactors; the catalog has **166 skills (including 15 opt-in personas), 382 technical reference leaves and 20 installation profiles**. A single authoring contract applies to every skill, without maturity tiers. This is a **documentation and deterministic-CI milestone**, not proof of production correctness, skill-routing quality or improvement in real agent outcomes. Next: fix observed discovery limitations and run held-out baseline-vs-toolkit evaluations.

## Why

The number of skills in a repository should not determine the cost of every agent session:

- **166 skills stored** in the library; only **5–20 installed** in a project profile.
- **Names, descriptions and task keywords** enable local discovery; only 1–3 relevant skill bodies should be read in a typical task.
- **Risk-aware workflows** prevent costly multi-agent review loops on trivial edits.
- **Validation and tests** run without using any LLM tokens.
- **No automatic third-party downloads or execution**; security and licensing come before convenience.

## Quick start

Requirements: Python 3.12+ and PyYAML.

~~~bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v

# Find focused skills and an advisory workflow mode
python scripts/skillctl.py search "Python DDD clean architecture" --profile python-backend
python scripts/skillctl.py recommend "AWS IAM migration" --profile cloud-engineering
python scripts/skillctl.py profiles
python scripts/skillctl.py show python-ddd
python scripts/skillctl.py references aws-bedrock
python scripts/skillctl.py read-ref aws-bedrock references/converse-api.md

# Measure only the reference that is explicitly opened
python scripts/context_budget.py --profile aws-platform --activated aws-bedrock --reference aws-bedrock:references/converse-api.md

# Compare approximate always-on context sizes
python scripts/context_budget.py --all

# Safe local installation: preview first, then copy
python scripts/install_profile.py --agent codex --profile python-backend --project /path/to/project
python scripts/install_profile.py --agent codex --profile python-backend --project /path/to/project --apply

# For Claude Code use --agent claude; no overwrite of existing installed skills
~~~

The installer writes only when `--apply` is provided. It copies selected skills to `.agents/skills` (Codex) or `.claude/skills` (Claude Code). Copy/adapt `AGENTS.md` into a target project separately to adopt shared conventions. Never install every profile indiscriminately.

## Operational persona skills (explicit opt-in)

Fifteen **self-contained, source-independent behavior protocols** in `skills/personas/` provide focused operating modes: deep interviews, adversarial critique/testing, repository archaeology, scope control, plan orchestration, product strategy, review adjudication, reliable handoffs, incident response, decisions, mentoring, **engineering leadership, privacy governance and cross-media branding** (logos, video storyboards and promotional campaigns). These are **not** duplicative framework/API references or automatically enabled subagents. They have no external reference leaves: the full operational method is in each selected `SKILL.md`. Install only the requested persona with `--skill`; selecting one does not override security, owner authorization or the chosen light/standard/deep workflow.

~~~bash
# Inspect before applying; no existing profile needs to grow
python scripts/skillctl.py show grill-master
python scripts/install_profile.py --skill grill-master --agent codex --project /path/to/project
python scripts/install_profile.py --skill grill-master --agent codex --project /path/to/project --apply
~~~

See [persona design, activation boundaries and evaluation criteria](docs/persona-protocols.md). A branding-lead coordinates creative identity and promotional media, while design/brand-identity-visualization and design/interaction-motion retain their distinct execution scopes.

## UI library expertise

35 optional provider skills across web, native and Flutter; plus one `ui-component-research` skill. The original `ui-library-selection` is **extended** in `skills/stacks`, never duplicated. See [UI skills](docs/ui-skills.md). Install only the chosen provider using `--skill` and read its optional references when needed.

## Explore

- [Progressive expertise refactor and quality standard](docs/progressive-expertise.md)
- [Historical expertise audit and current evaluation backlog](docs/expertise-audit.md)
- [Opt-in persona protocols and governance](docs/persona-protocols.md)
- [Design refactor decision matrix and evidence](docs/design-refactor-audit.md)
- [Growth skill audit, experimentation and lifecycle governance](docs/growth-refactor-audit.md)
- [Stack selection audit and identity solution boundaries](docs/stacks-refactor-audit.md)
- [Design product experience specialists and chart-provider boundaries](docs/design-product-skills.md)
- [Catalog and authoring conventions](docs/catalog.md)
- [Progressive disclosure and token budgets](docs/skill-routing.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security and third-party intake](SECURITY.md)

The library covers Python DDD and hexagonal architecture, API design, modern Python and TypeScript, AWS/GCP/Azure/Cloudflare and IaC, data engineering, LLM applications, UI/UX and glassmorphism, testing, security and release workflows.

## Development policy

Open a focused feature branch and PR. CI validates skill metadata/profile references, runs unit and selected integration tests, and enforces a **rough** context-budget guardrail; it does **not** validate every provider API, deployed behavior or model-agent outcome. Never push directly to `main`. **A green CI and mergeable PR are necessary checks, not merge authorization: merge into `main` only after the repository owner's explicit approval.** See [Contributing](CONTRIBUTING.md) and the [evaluation roadmap](docs/roadmap.md).

Original content is MIT licensed. Third-party sources such as [ECC](https://github.com/affaan-m/ECC), [Superpowers](https://github.com/obra/superpowers), [Anthropic Cybersecurity Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) and [Brag](https://github.com/latent-spaces/brag) inspired the architecture; **none of their skills are copied into the project at this stage**.

## Design craft and growth (optional)

Source-curated visual craft and motion references enhance existing design skills; new opt-in content strategy, technical SEO, AI search visibility, brand-board visualization and requirements discovery skills have narrow independent triggers. Install via a focused profile or individual --skill:

~~~bash
python scripts/install_profile.py --profile design-craft --agent codex --project /path/to/project
python scripts/install_profile.py --profile growth-marketing --agent claude --project /path/to/project
python scripts/skillctl.py references interaction-motion
python scripts/skillctl.py read-ref interaction-motion references/easing-and-implementation.md
~~~

All commands preview installations by default. No external scripts are executed or external source data copied; see [selection and pinned provenance](docs/design-growth-source-review.md). Do not treat AI visibility as a guaranteed ranking or inclusion mechanism.

## Python production engineering and LLM providers

Python V2 adds focused expertise on application architecture, HTTPX clients, SQLAlchemy persistence, observability, FastAPI lifecycle, async/worker capacity, cloud-native AI inference and LangChain/LiteLLM tradeoffs. **The catalog keeps one narrow activated SKILL.md and selectively read deep references**, instead of loading all Python/provider material for a simple bug fix.

~~~bash
python scripts/skillctl.py search "FastAPI lifespan Pydantic HTTPX" --profile python-backend
python scripts/skillctl.py search "Azure Foundry Responses" --profile python-llm-production
python scripts/skillctl.py references python-llm-gateways
python scripts/skillctl.py read-ref python-llm-gateways references/litellm-routing.md
python scripts/context_budget.py --profile python-llm-production --activated python-llm-gateways --reference python-llm-gateways:references/litellm-routing.md
~~~

See [Python architecture and stack decision matrix](docs/python-engineering-v2.md) for lightweight vs production choices and official provider docs. Provider-specific model IDs, quotas, SDK versions and endpoints require verification in the target project; docs are not deployment authorization.

## Quality engineering (risk-based, primary-source reviewed)

Seven focused Quality specialists cover testing, code security, dependency
supply chains, performance profiling, release decisions, GitHub PR workflows
and adversarial external-skill intake. Their activation pages selectively route
to **21 local deep reference leaves** (19 added in this refactor). The documented
method uses pytest/Playwright/Hypothesis, OWASP ASVS, NIST SSDF, GitHub security
guidance, SLSA, Python cProfile and k6 as appropriate; it does not load all
Quality materials for a routine code edit.

~~~bash
python scripts/skillctl.py search "pytest integration contract regression"
python scripts/skillctl.py references secure-code-review
python scripts/skillctl.py read-ref secure-code-review references/threat-boundaries-asvs.md
python -m unittest discover -s tests -p 'test_quality_contract_examples.py' -v
~~~

See [Quality audit, citations and evidence limitations](docs/quality-refactor-audit.md).
Source guidance is linked, not executed. A green structural CI is not
proof of a production penetration test, load SLO or live cloud IAM.

## Architecture expertise (source-reviewed)

Eight existing Architecture skills were refactored without adding generic
or duplicate skills. **24 selectively indexed local references** cover
API/RFC/OpenAPI/AsyncAPI contracts, ADRs, domain boundaries, DDD,
ports/adapters, modular monoliths, event delivery/outbox/sagas,
technology decisions, benchmark evidence and reversible migrations.

~~~bash
python scripts/skillctl.py search "transactional outbox event saga"
python scripts/skillctl.py references event-driven-design
python scripts/skillctl.py read-ref event-driven-design references/outbox-inbox-and-idempotency.md
python scripts/check_architecture_boundaries.py --root examples/architecture_boundaries --config examples/architecture_boundaries/boundaries.json
python -m unittest discover -s tests -p 'test_architecture_boundaries.py' -v
~~~

Official source decisions and limitations:
[Architecture category audit](docs/architecture-refactor-audit.md).
The checker is for explicit Python import restrictions, **not a
general proof of software architecture**. No user-count-based
"microservices required" rule exists.

## Backend production engineering (Python + Node TypeScript)

Seven existing Backend skills now own **33 selectively readable references**
(15 additional). They cover modern Python packaging/uv, FastAPI lifecycle,
HTTPX retries/deadlines, SQLAlchemy isolation/async sessions, OpenTelemetry,
Celery worker reliability and Node/TypeScript runtime/API behavior.
Architecture, Quality and cloud/LLM concerns remain independently routed.

~~~bash
python scripts/skillctl.py search "TypeScript Node.js API runtime validation"
python scripts/skillctl.py references typescript-api
python scripts/skillctl.py read-ref typescript-api references/runtime-schema-and-security.md
node --test examples/backend-typescript/tests/*.test.ts  # Node 24+
python -m unittest discover -s tests -p 'test_backend_expertise.py' -v
~~~

[Official-source Backend audit](docs/backend-refactor-audit.md) distinguishes
current provider semantics from illustrative code and unverified deployment
claims. The Node example requires a separate strict TypeScript typecheck
before production and is deliberately not a real authenticated service.

## Data engineering — source-verified domain expertise

Data contains **7 focused skills**: four strengthened (pipeline quality,
relational design, PostgreSQL performance, schema migration) plus three
new independent specialists (analytics modeling, lakehouse/warehouses,
CDC and stateful streaming). Each activates only the relevant skill and
reference leaves. **22 local references** cover dbt, Airflow, GX,
PostgreSQL, Iceberg/Parquet, Snowflake, BigQuery, Debezium and Flink.

~~~bash
python scripts/skillctl.py search "dbt dimensional grain metrics"
python scripts/skillctl.py references streaming-cdc-engineering
python scripts/skillctl.py read-ref streaming-cdc-engineering references/debezium-cdc-and-wal.md
python -m unittest discover -s tests -p 'test_data_replay_contract.py' -v
# Disposable PostgreSQL integration tests also run in GitHub CI
~~~

The [Data audit](docs/data-refactor-audit.md) records first-party official
sources, tested contract semantics and unverified production/cloud work.
A green route test, DAG parse or SQL schema check is **not** proof of
live Snowflake/BigQuery pricing, CDC recovery or universal correctness.

## AI engineering — source-verified agents, retrieval and MCP

Eight AI specialists provide **26 individually indexed deep references**:
five existing skills refactored for typed provider behavior, tool
authorization, LLM evaluations, RAG assessment and LiteLLM governance;
three new independently triggered specialists for **agent orchestration,
RAG implementation and MCP protocol integration**.

~~~bash
python scripts/skillctl.py search "mcp protocol server client transport oauth"
python scripts/skillctl.py references agent-orchestration
python scripts/skillctl.py read-ref agent-orchestration references/state-checkpoints-and-replay.md
python -m unittest discover -s tests -p 'test_ai_security_contract.py' -v
~~~

See [AI technical/source audit](docs/ai-refactor-audit.md). MCP's
2026-07-28 released stateless specification and SDK compatibility are
reviewed; LangGraph checkpointers do not guarantee exactly-once external
effects, and LiteLLM Proxy budgets require a functioning database.
All examples are offline and must not be deployed as credentialed agents.

## Cloud services — provider-specific production playbooks

**41 Cloud skills** (22 new service specialists) have **82 on-demand reference
leaves** for authentication, SDK, minimum permissions, diagnostics,
rate limits and recovery. A narrow service selector avoids blindly
loading the AWS, GCP, Azure and Cloudflare documentation together.
Opt-in installation profiles: `aws-platform` (20), `gcp-platform`
(15), `azure-platform` (15) and `cloudflare-edge` (12).

~~~bash
python scripts/skillctl.py search "GCP Cloud Run OIDC invoker"
python scripts/skillctl.py references azure-service-bus
python scripts/skillctl.py read-ref azure-service-bus references/connection-and-permissions.md
python scripts/context_budget.py --profile gcp-platform --activated gcp-cloud-run --reference gcp-cloud-run:references/connection-and-permissions.md
~~~

See [cloud service-by-service connection map](docs/cloud-service-map.md)
and [official-source audit](docs/cloud-refactor-audit.md). Reading skills
**does not authenticate** an agent to cloud resources or authorize
resource creation. Production requires owner-approved IAM/network/test.

## Frontend framework engineering

Seven focused frontend skills have 21 selectively readable deep references on React, Next.js, TanStack Start, Vue/Nuxt, Svelte/SvelteKit, Angular and Astro. The legacy combined Vue/Svelte skill was replaced rather than duplicated. A new 18-skill frontend-platform discovery profile is opt-in.

~~~bash
python scripts/skillctl.py search 'TanStack Start serverfunctions middleware csrf'
python scripts/skillctl.py references tanstack-start
python scripts/skillctl.py read-ref tanstack-start references/start-server-functions-auth.md
node --test examples/frontend-boundaries/tests/*.test.mjs
~~~

[Frontend framework map](docs/frontend-framework-map.md) and [official source audit](docs/frontend-refactor-audit.md). The Node boundary example tests an educational server, not a real framework runtime; each production app still needs its own pinned typecheck/build and browser E2E.

## UI: production component contracts without template-shaped design

35 existing component-library specialists remain **opt-in** with two
deep references each, now with vendor-specific version/composition
warnings. The common ui-component-research has five leaves including
upgrades, licensing and release tests. Existing frontend-design has a
new art-direction and critique leaf: audience and authentic product
content drive layout/typography; defaults and demo themes are scaffolds.

[UI production rubric](docs/ui-production-quality.md) ·
[Source and GitHub skill audit](docs/ui-refactor-audit.md) ·
[Contrasting design briefs](evals/ui-visual-briefs.yaml).
Do not automatically import outside skills or claim a page is visually
validated without viewing rendered screenshots.
