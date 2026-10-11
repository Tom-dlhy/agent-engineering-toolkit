# Managed PostgreSQL, SQLite-family edge databases and runtime constraints

Read when: deciding where to deploy the selected engine or comparing Neon/Postgres, Cloudflare D1 and other remote/edge-managed options.

## Engine != provider != plan
A PostgreSQL-compatible SQL service has shared SQL semantics but still differs in connection handling, cold-start, backups/PITR, branching, regional placement, data egress and cost. A SQLite-compatible remote API is not necessarily a local SQLite file. Verify plan/version/region and the specific driver's protocol (TCP / HTTP / WebSocket / Workers binding).

### Evaluation checklist
| Concern | PostgreSQL managed e.g. Neon/RDS/Cloud SQL | D1 or other edge SQLite-family |
|---|---|---|
| Runtime | TCP/HTTP driver, TLS, serverless pooler behavior | Runtime binding/client, edge request semantics |
| Connection model | Pooled vs direct DB URL; max connection, transaction/session affinity | Provider query binding and per-database concurrency |
| Multirow writes | Full DB transaction support (dialect + driver) | Verify exact provider API's transaction/batch guarantees |
| Scale | Storage, CPU/compute, connection pressure, replicas | Database-per-tenant strategy, per-database throughput, row size |
| Recovery | Backups/PITR and verified restore by tier | Provider time-travel and restore limits by tier |
| Migration | Native tools extensions, lock/grants, direct migration connection | SQLite dialect migration constraints and unsupported SQL |
| Lock-in | Postgres export portability vs provider-specific ops | API bindings, replication and SQLite portability differ |

**Concrete official limitation (2026-04-21, not immutable):** Cloudflare D1 limits page documents that each database processes one query at a time and has a bounded database size and queue/overload behavior. Do **not** reduce this to a fake "global D1 QPS" guarantee; duration and partitioning matter. Source: https://developers.cloudflare.com/d1/platform/limits/.

Neon managed PostgreSQL has different direct and pooled connection strings; migrations and session-scoped behavior may require a direct connection where transaction pooling interferes. Validate official current Neon docs and project driver. Avoid asserting a universal free-plan capacity or zero-cold-start latency without checks.

## Evidence to collect in a sandbox
1. Deploy a representative route/worker and run exact driver/ORM adapter against the target tier.
2. Verify a concurrent transaction, failed transaction rollback and correct post-write consistency.
3. Test query/connection saturation and serverless cold path in target region with modest authorized fixture load.
4. Measure backup restore and schema evolution (not just an advertised check box).
5. Confirm RPO/RTO, encryption/residency/compliance evidence, monitoring and billing export.

Sources: https://developers.cloudflare.com/d1/platform/limits/ and https://neon.com/docs/connect/connection-pooling and https://www.postgresql.org/docs/18/transaction-iso.html
