# Quality attributes and falsifiable architecture rules

**Read when:** scalability, reliability, security, maintainability,
portability or recovery is used to justify a design choice.

## Convert quality talk into observable scenarios

| Attribute | Example evidence | Hidden tradeoff |
|---|---|---|
| Reliability | SLO useful-task success, RTO/RPO drill | Operational cost/redundancy |
| Performance | p95/p99 under specified workload + errors | Caching vs consistency |
| Security | Tenant isolation negative test, IAM boundaries | Overheads and platform ownership |
| Modularity | Enforced module imports, contracts | Indirection and duplicated adapters |
| Operability | Traces spanning provider, DB and queue | Telemetry cost/data protection |
| Portability | Demonstrated second adapter or migration | Provider-native feature fidelity |
| Cost | € per *completed useful task*, including operators | Latency/quality/incident reserve |

A measurable scenario has stimulus, environment, response and bound:
"For synthetic concurrent orders at X arrivals/s, p95 successfully
committed calls below Y ms, unauthorized cross-tenant writes zero."
Choose X/Y from measured user needs, not a generic "10k users" rule.

## Fitness functions

- Static import check: domain may not import DB/HTTP/LLM SDK.
- Contract suite: old and new consumer wire contracts still pass.
- Failure drill: after crash between publish/ACK, one durable
  business effect following redelivery.
- Data isolation: tenant B cannot see or update tenant A record.
- Recovery: restore a real staging backup under defined RTO/RPO.
- Architecture change guard: module import direction remains valid.

None of these alone certifies a style. Static architecture tests
demonstrate a constraint, not business correctness or production
scaling.

## Record uncertainties

An ADR should link measurement scripts and results at a revision,
plus the exact question an unrun test leaves unresolved.
A favorable marketing claim about eventual consistency or "high
performance" without workload evidence is not sufficient.

Sources: https://learn.microsoft.com/en-us/azure/well-architected/ ,
https://sre.google/sre-book/service-level-objectives/ ,
https://learn.microsoft.com/en-us/azure/architecture/guide/ .
