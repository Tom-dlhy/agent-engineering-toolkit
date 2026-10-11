---
name: technology-tradeoffs
domain: architecture
version: "0.1.0"
description: >-
  Use when comparing libraries, deployment models, database technologies or buy-versus-build options under real constraints. Do not use just to defend a preferred framework.
---

# technology-tradeoffs

## Evidence
Collect requirements, nonfunctional constraints, maintainers' expertise, licensing, dependency freshness, API stability and 3-year maintenance burden. Validate fast-changing claims against official documentation.
## Compare
Create a small matrix: developer experience, operational complexity, security, performance, cost, portability and reversibility. Use realistic workload sizes and benchmark critical unknowns rather than star counts.
## Decide
Recommend a default plus second-best alternative. Document key reasons, conditions that would overturn the recommendation and incremental migration/rollback.
## Anti-patterns
Do not prefer "latest" automatically, invent scalability figures or introduce additional tooling without a clear benefit.
