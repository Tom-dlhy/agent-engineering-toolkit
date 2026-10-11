# Agent Engineering Toolkit

**Vendor-neutral AI engineering skills, workflows and quality gates — modular by design, economical in context.**

A growing library of **113 first-party skills across 12 domains**, with **16 small installation profiles**, lightweight `light / standard / deep` workflows, optional agent role briefs, and a **deterministic local skill finder**. Designed for Claude Code, Codex and other compatible environments without requiring an LLM API call to discover skills.

> Status: a single skill-quality contract applies to all 113 catalog entries. Depth and real-world verification remain uneven across domains; inclusion in the catalog and passing structural CI are not evidence of production expertise. Refactoring proceeds domain by domain without maturity tiers.

## Why

The number of skills in a repository should not determine the cost of every agent session:

- **113 skills stored** in the library; only **5–20 installed** in a project profile.
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

## UI library expertise

35 optional provider skills across web, native and Flutter; plus one `ui-component-research` skill. The original `ui-library-selection` is **extended** in `skills/stacks`, never duplicated. See [UI skills](docs/ui-skills.md). Install only the chosen provider using `--skill` and read its optional references when needed.

## Explore

- [Progressive expertise refactor and quality standard](docs/progressive-expertise.md)
- [Expertise depth audit / migration backlog](docs/expertise-audit.md)
- [Catalog and authoring conventions](docs/catalog.md)
- [Progressive disclosure and token budgets](docs/skill-routing.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security and third-party intake](SECURITY.md)

The library covers Python DDD and hexagonal architecture, API design, modern Python and TypeScript, AWS/GCP/Azure/Cloudflare and IaC, data engineering, LLM applications, UI/UX and glassmorphism, testing, security and release workflows.

## Development policy

Open a focused feature branch and PR. CI validates all skill metadata/profile references, runs unit tests and enforces a **rough** context-budget guardrail. Never push directly to main. Merge only after required checks pass.

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
