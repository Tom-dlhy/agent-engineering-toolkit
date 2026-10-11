# Architecture style selection: when complexity pays off

**Read when:** comparing a layered service, modular monolith,
web-queue-worker, microservices, event-driven system or CQRS.

| Style | Suitable | Costs |
|---|---|---|
| Small layered app | One team/deploy; simple domain | Horizontal folders can sprawl |
| Modular monolith | Growing bounded capabilities, same deploy | Must enforce module imports/contracts |
| Web-queue-worker | Long/bursty workloads | Durable jobs, retries, queue operations |
| Microservices | Real independent domain teams/deployment/fault isolation | Network, tracing, distributed consistency |
| Event-driven | Many async independent consumers | Duplicates, latency, order, observability |
| CQRS/read projection | Writes/reads have truly different consistency/scale needs | Lagging views and duplicate pipelines |

Microsoft Azure Architecture Center explicitly states microservices
increase total architecture and operational complexity even if
each service is smaller. A single-deploy modular monolith can
replicate horizontally and often scales adequately; architecture
is not prescribed by registered user count.

## Example — LLM document processing

A single team building extraction with variable 90s model
latency can use one API and **durable** background worker backed
by job status and an existing DB. This is not automatically a
microservices system. Quotas TPM/RPM, request payload, DB
connections and job p99 determine scaling bottlenecks.
Events help if independent consumers need business notifications.

## Distributed consequences

Network chains increase tail latency and failure fanout.
Data-per-service creates asynchronous consistency challenges;
sharing a database across independently deployed services
weakens autonomy. Distributed transactions can require sagas
and compensations, which don't provide full ACID isolation.

## Test the trade-off

Map which invariant must be immediately consistent and how
it crosses modules/services. Simulate dependency outage,
duplicate messages and schema skew if distributed style is
chosen. Record rollback and operational staffing as first-class costs.

Sources:
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles ,
https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-patterns.html .
