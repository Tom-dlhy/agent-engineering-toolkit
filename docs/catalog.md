# Skill catalog and design conventions

The source of truth is `registry/skills.yaml`: 163 first-party skills grouped into 13 domains (12 technical domains and one opt-in behavioral-persona domain).

| Domain | Focus |
| --- | --- |
| `core` | Routing, verification, debugging and authoring |
| `architecture` | DDD, ports/adapters, modularity, events and contracts |
| `backend` | Python, TypeScript, FastAPI and background processing |
| `frontend` | React, TanStack Start, Next.js, Vue and Svelte |
| `stacks` | Cross-layer stack, database, UI library and authentication solution selection |
| `design` | Art direction, flows, information architecture, content, charts, UX and accessibility |
| `cloud` | AWS, GCP, Azure, Terraform, Cloudflare, Kubernetes, FinOps, SRE |
| `data` | Data quality, SQL, migrations and performance |
| `ai` | LLM adapters, RAG evaluation, model evals and secure agents |
| `quality` | Testing, code review, dependencies, releases and PR workflows |
| `ui` | Provider-specific React/Vue/Angular/Svelte/mobile component guidance |
| `growth` | Editorial governance, SEO/AI search observation, experiments and lifecycle retention |
| `personas` | Explicitly activated interview, critique, coordination, adversarial evaluation, incident, decision and teaching protocols |

## Minimal interface of a skill

~~~yaml
---
name: skill-name
domain: category
version: "0.1.0"
description: >-
  Use when ... . Do not use when ... .
---
~~~

The content is a **method**: scope, prerequisites, procedure, verification and failure modes. It should not merely say "act as a world-class expert".

Only name/description metadata is needed to decide whether to read the body. Technical deep details normally belong in skill-local `references/`; **persona skills are an intentional exception**: their complete behavior protocol is self-contained in `SKILL.md`, with no required external reference file. Scripts, when present, must be permission-scoped, deterministic and reviewed.

## Importing third-party skills

No third-party skills have been copied into this release. We studied Superpowers, ECC and specialized repositories for inspiration but wrote the shipped skills from scratch.

Before vendoring outside skills, record exact source commit, license and notices, inspect scripts and transitive dependencies, validate names and triggers, measure context and run targeted behavior evaluations. `registry/sources.lock.yaml` is reserved for this work. An audited importer and upgrade process remain on the roadmap.

## Uniform quality standard

Every skill follows the same authoring, verification and security criteria. The optional frontmatter `version` is a content revision marker, not an expertise tier. No `maturity` property exists in the registry, and selection is determined by task relevance and profile availability. See [Core governance](core-refactor-audit.md).
