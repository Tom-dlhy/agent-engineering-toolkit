# Google Cloud SQL for PostgreSQL — operations and recovery verification

**Read when:** selecting production capacity, cost, rollback, monitoring or integration failure behavior.

## Service-specific engineering
Pool connection fanout, auth token/DB TLS, instance/project mismatch, private IP/VPC egress, failover connections, migration/version compatibility, PITR/backups and read replica lag. Avoid DB master account in app.

## Identity and resilience constraints
Service account with Cloud SQL Client role + Cloud SQL Connector using ADC; DB credentials/role (or IAM DB auth if configured) remain separate from Google IAM. `roles/cloudsql.client` for connector; database user/privileges separate, use Secret Manager or IAM database authentication configuration. Private IP requires network reachability/VPC setup; connector isn't bypass of private routing.

Measure p95/p99 latency, error/queue backlog, resource limits, regional availability, quota project and relevant billable units. A successful local SDK call is not proof of end-to-end authorization, service-to-service JWT identity or failover. For mutations, treat post-send network timeout as **unknown remote outcome** and reconcile before retry; use per-service preconditions/deduplication features where documented.

## Required negative and integration tests
1. Wrong project/region and revoked service-account grant cause deterministic denial.
2. Expired/incorrect identity and wrong resource produce safe error mapping, no credentials in logs.
3. Duplicate/reordered input, timeout after remote commit and cancellation preserve application invariant.
4. Provider regional quota/throttle and network fault trigger bounded retries or fail-closed result.
5. Production claim requires authorized sandbox check of actual IAM, configuration, SDK version and rollback procedure.

## Official docs
- https://docs.cloud.google.com/sql/docs/postgres/connect-connectors
- https://docs.cloud.google.com/sql/docs/postgres/connect-run
