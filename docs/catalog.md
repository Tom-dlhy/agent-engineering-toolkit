# Skill catalog and design conventions

The source of truth is `registry/skills.yaml`: 59 first-party skills grouped into 10 domains.

| Domain | Focus |
| --- | --- |
| `core` | Routing, verification, debugging and authoring |
| `architecture` | DDD, ports/adapters, modularity, events and contracts |
| `backend` | Python, TypeScript, FastAPI and background processing |
| `frontend` | React, TanStack Start, Next.js, Vue and Svelte |
| `stacks` | Stack, database and UI library selection |
| `design` | Design systems, typography, glass, bento, UX and accessibility |
| `cloud` | AWS, GCP, Azure, Terraform, Cloudflare, Kubernetes, FinOps, SRE |
| `data` | Data quality, SQL, migrations and performance |
| `ai` | LLM adapters, RAG evaluation, model evals and secure agents |
| `quality` | Testing, code review, dependencies, releases and PR workflows |

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

Only name/description metadata is needed to decide whether to read the body. Additional details belong in skill-local `references/`, while scripts must be permission-scoped, deterministic and reviewed.

## Importing third-party skills

No third-party skills have been copied into this release. We studied Superpowers, ECC and specialized repositories for inspiration but wrote the shipped skills from scratch.

Before vendoring outside skills, record exact source commit, license and notices, inspect scripts and transitive dependencies, validate names and triggers, measure context and run targeted behavior evaluations. `registry/sources.lock.yaml` is reserved for this work. An audited importer and upgrade process remain on the roadmap.
