# Migration strategy, restore drills and fair DB selection benchmarks

Read when: recommending a different database from the one already deployed, checking cloud exit risk or validating data correctness under concurrency.

## Admission gate: when NOT to migrate
If current engine meets core constraints and observed workloads, migration is normally a cost with little guaranteed gain. First consider query/index/migrations improvements through relevant data skills. Require a falsifiable reason to switch: unsupported transaction model, residency, unacceptable recovery, real performance bottleneck or operational cost with evidence.

## Cross-engine change risk
- SQL dialect, types, indexes, constraints, sequences and UTC/date semantics can differ despite ORM compatibility.
- Collation, casefolding, nullable uniqueness, JSON indexing and query plans may produce different outputs.
- Application-level auth/tenant policies must be revalidated against DB RLS and service boundaries.
- Data export/import may break generated IDs, foreign keys, revisions, object references and audit timestamps.
- Managed service migrations may require direct network paths, IAM, extension/version compatibility and outage/maintenance window.

## Bounded testing contract
~~~yaml
scenario: replace existing primary data store (illustrative)
before:
  - backup verified with actual restore
  - migration dry-run on sanitized representative size and schema
tests:
  - invariant preserving concurrent writes
  - deterministic reconciliation count plus key-level checks
  - index and query latency p50/p95 under realistic read/write ratio
  - changed schema rollout with old and new client versions
  - read-after-write and outage recovery
  - forbidden tenant access blocked
after:
  - retain rollback window and old data integrity
  - operations owner monitors locks, errors, storage and spend
~~~
Never take a cost-per-query benchmark from one free account and call it fair to a dedicated production cluster. Record load generator, region, CPU tier, DB size, data distribution, hot keys, warm-up, test duration and percentile distribution. Avoid stress on third-party services without authorization.

## RPO/RTO are verified behaviors
RPO expresses tolerated **data loss window**, RTO tolerated **recovery time**. A provider claiming daily backups doesn't prove RPO minutes or that app/permissions recover within RTO. Run a controlled restore exercise using authorized, synthetic data; record time, restored identity and post-restore integrity.

## Responsibility
`database-selection` decides **whether/which** engine/service; `data/schema-migrations` handles schema rollout; `cloud/<provider>` handles service operations; `quality/release-readiness` gates production.

Sources: https://www.postgresql.org/docs/current/backup.html and https://developers.cloudflare.com/d1/platform/limits/ and https://docs.aws.amazon.com/wellarchitected/latest/framework/reliability-pillar.html
