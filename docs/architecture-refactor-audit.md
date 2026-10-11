# Architecture category — source-verified technical refactor

Review date: **2026-10-11**. Governance source: user-maintained
Agent Engineering Toolkit Charte de gouvernance et d'évolution v2.
Base: main after Core #13 and Quality #14, both merged.

## Decision and scope audit

**Eight existing skills, none added or deleted.** Reuse-first charter rules
apply. The priority is expertise in **selection**, **implementation** and
**falsification**, not pattern name-dropping. No maturity labels/ranks.

| Skill | Previously missing or thin | Action and independent responsibility |
|---|---|---|
| api-contract-design | ~1 KB: HTTP semantics, versions and schema compatibility vague | EXTEND; 3 references for HTTP/RFC, OAS and async/webhooks |
| architecture-decision | ~1 KB: ADR method without empirical fitness | EXTEND; 3 references for ADR, styles and quality attributes |
| event-driven-design | ~1 KB: outbox/saga list without failure windows | EXTEND; 3 references for contracts, outbox/inbox, sagas |
| hexagonal-architecture | Existing 2 Python leaves | EXTEND and preserve; add adoption/enforcement |
| modular-monolith | ~1 KB: boundary principles but no tests/migration | EXTEND; 3 references for ownership, transactions, extraction |
| python-project-architecture | Existing 3 technical leaves | REFINE activation; preserve domain depth |
| python-ddd | Existing 2 domain/UoW leaves | EXTEND; add context mapping and consistency |
| technology-tradeoffs | ~1 KB: comparison summary | EXTEND; 3 references for evidence, POC/TCO, lock-in |

**17 new targeted reference leaves**, giving **24 indexed Architecture
references** (3 per skill); the previously useful 7 remain. Three references
per skill reflect this domain refactor, **not a forced quota for other
categories**.

### Responsibility and overlap decisions

- architecture-decision = record a consequential systemic decision/ADR;
  technology-tradeoffs = collect and compare current concrete products,
  libraries, cost and provider limitations. A major technology choice may
  use the first *after* the second; not two competing arbitrators.
- python-project-architecture = Python package/module organization.
  modular-monolith = cross-language business module autonomy and one deploy.
  python-ddd = domain semantics/aggregates/context map.
  hexagonal-architecture = inward ports/adapters and dependency direction.
- api-contract-design = published client/event contract. event-driven-design
  = delivery/replay/failure semantics and distributed workflow consistency.
- No duplicate FastAPI, HTTPX, SQLAlchemy, worker or AWS skill is introduced.

## Confirmed source corrections and nuanced decisions

### Architecture style — Microsoft Azure Architecture Center

[Style selection](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles)
and [microservices](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
describe constraints, independent deployment, domain boundaries and
tradeoffs. Microservices **increase distributed complexity, operational
cost, network hops and data consistency risks**. A modular monolith can be
appropriate at scale; user count alone cannot select architecture.

### Ports and domain integration — AWS

[AWS Hexagonal pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)
explains testable domain/application separation from infrastructure.
[Anti-corruption layer](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/acl.html)
translates different bounded-context semantics but adds a migration
dependency/latency; it is not always required or permanent.

### Event delivery and distributed state — AWS and Microsoft

[Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
atomicizes **DB state and intent to publish**, not publisher/broker/consumer
global exactly-once side effects. A publisher that crashes after sending
but before marking delivered can resend; durable dedupe is needed.

[Saga patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-patterns.html)
compare choreography and orchestration; compensation is a new business
action and sagas lack isolation of a single ACID transaction.

### Modern API specs and RFCs

- [OpenAPI specification index](https://spec.openapis.org/oas/):
  **OpenAPI 3.2.1** appears among published versions at research time;
  adoption is bounded by actual generator and validator support.
- [RFC 9110 HTTP](https://www.rfc-editor.org/rfc/rfc9110.html):
  GET/HEAD safe, PUT/DELETE and safe methods idempotent in intended
  effects; unsafe methods need explicit retry semantics.
- [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html):
  standardized application/problem+json errors; replaces RFC 7807.
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12):
  format and vocabulary behavior depend on chosen validator/setting.
- [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0):
  machine-readable channels/messages/operations, *not* guaranteed
  durable processing semantics.
- [GraphQL specification](https://spec.graphql.org/):
  typed query surface; authorization/query-cost are runtime obligations.

### ADR and quality evidence

[ADR community documentation](https://adr.github.io/) gives a
lightweight context/decision/consequences record. [Microsoft Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/)
and [Google SRE SLOs](https://sre.google/sre-book/service-level-objectives/)
guide measurable scenario/fitness attributes. These sources support
method choices, **not** made-up user-count thresholds.

**SOTA means version-aware, source-checked and adaptable**, not claiming
that a style is always best or that reading a vendor page verifies
a live cloud account.

## Implemented execution evidence

- New **scripts/check_architecture_boundaries.py** reads explicit JSON
  package rules and checks Python AST import statements without network.
  Existing allowed Orders→Billing public import passes. Tests inject
  forbidden absolute/relative imports, framework dependency leakage and
  syntax failure into temporary copies. This is static import evidence
  **only**, not a complete dependency/architecture proof.
- **tests/test_architecture_boundaries.py**: 7 executable positive/negative
  checks for this checker.
- **evals/architecture-routing.yaml**: eight positive selection queries,
  six negative neighboring tasks and no-match cases.
- **tests/test_architecture_expertise.py**: ref depth, single quality
  contract, 8-skill registry, routing, path traversal, selected reference
  context budget and source provenance.
- Existing global toolkit tests, FastAPI example and all profile budget
  guards remain in CI.

## Limitations and follow-up

No authorized live microservice deployment, synthetic load benchmark,
PostgreSQL transactional outbox end-to-end test, human ADR workshop or
cloud provider proof was performed. Source-derived recommendations
were reviewed against official primary sources; they remain dependent
on actual project architecture, versions and business semantics.

A **green CI verifies documented structural and executable boundary
conditions**. It does not certify that an LLM host will activate the
optimal skill on held-out prompts nor that all architecture choices
will be production-correct. Those need task-level behavioral evals
and real-system scenario tests. No merge without user permission.
