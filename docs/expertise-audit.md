# Skill depth audit — phase 1, 2026-10-11

## Baseline and scope

The inherited `feat/modular-skill-engine` branch has **59 first-party skills**, approximately **1.1 KiB/skill on average**, with **zero local reference files or examples**. This is a capable routing foundation, **not** a technically exhaustive skill library. The UI-specific [PR #9](https://github.com/Tom-dlhy/agent-engineering-toolkit/pull/9) remains open independently and is **not** included in this branch.

Phase 1 keeps the original 59 entries, refactors the broad `aws-integration` skill into a cross-service coordinator, and adds six independently activated service skills. Therefore this branch contains **65 catalog entries**, but **only seven are marked `expert-v2`**. Every other technical skill is explicitly pending deeper work. This document does **not** claim that all 65 meet the final standard.

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

## Definition of an expert-v2 skill

- Narrow, uniquely activated scope with an explicit exclusion.
- A `SKILL.md` **capable of deciding**, not merely linking to documentation.
- At least two **real, locally present** deep leaves with clearly differentiated triggers.
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

Review each refactor on its own merits; no mechanical mass-generation or blanket `expert-v2` badges. Promotion to `expert-v2` requires human technical review in addition to static CI.

## Phase 2 addendum — UI integration into current main (PR #9)

The original PR #9 is now reconciled with main after PR #5 and PR #10 merged. The repository contains **101 unique skills**, including **35 opt-in UI library providers**, one shared `ui-component-research` and exactly one `ui-library-selection` under `skills/stacks`. UI-specific references: **70 local provider leaves + 4 shared component-family leaves + 1 selector map**. Existing seven AWS `expert-v2` specialists remain unchanged.

The 35 UI providers are marked `expanded-v2` (distinct from `expert-v2`): all have version-checking implementation and integration playbooks, but static validation is not evidence that every vendor API, full production workflow or accessibility behavior was tested against a live app. Some providers remain broad and need further version-pinned component examples and agent behavioral evaluation. Treat source citations as directions for freshness, not permission to assume current props.

Follow-up work: run representative benchmark apps for web, Vue/Angular/Svelte, React Native and Flutter, test a form/overlay/data table from each selected provider under the installed release, measure skill-selection errors, and promote selectively after review. Do not force all 35 into standard install profiles.
