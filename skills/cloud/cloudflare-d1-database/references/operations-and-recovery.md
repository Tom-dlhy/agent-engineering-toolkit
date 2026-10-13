# Cloudflare D1 SQLite database — release, limits, security and incident recovery

**Read when:** deploying, troubleshooting production behavior or validating security/consistency.

## Service-specific failure modes
D1 uses SQLite semantics, not PostgreSQL isolation or multi-tenant authorization by default. Bound query/row size, migration strategy, index/performance, read replication/session consistency, backup/restore and env preview DB separation.

### Sessions and read-after-write contract
When using D1 Sessions/read replication, `env.DB.withSession("first-primary")`
starts on the primary; `"first-unconstrained"` may start on a replica.
Use the same session for a write and its dependent read.

To continue across authenticated requests, carry the returned
`session.getBookmark()` (a string after queries, null before any query)
into the next request's `env.DB.withSession(bookmark)`; this preserves a
minimum observed database version. Validate the caller and object
authorization separately: a bookmark is **not** an authentication token.

If the required bookmark is lost, do not claim that continuity is unchanged.
Choose `first-primary` if a fresh primary read meets the requirement;
otherwise report the gap. Do not replay a mutation to recreate a bookmark.
Without D1 Sessions, queries use the primary rather than read replicas.

Test dependent read, bookmark propagation, missing-bookmark fallback and
unchanged tenant checks. A fake binding verifies the caller's decisions, not
the replica's actual consistency: verify that separately in an authorized
preview environment with the target runtime/API pinned.

Source reviewed 2026-10-13:
https://developers.cloudflare.com/d1/worker-api/d1-database/

## Trust and tenancy
Binding attached to Worker allows querying configured database; management/migrations via scoped Wrangler deployment account token. Never interpolate raw SQL query parameters, use `.bind()` and validate identifiers.

Runtime Access/Zero Trust controls are not equivalent to application authorization of objects. Synthetic tests should simulate a denied caller, wrong tenant, expired token, missing binding and preview/prod crossed configuration. Never return provider secrets, bearer tokens, raw signed URLs beyond intended audience or unrestricted storage objects.

## Scale and cost
Check actual official Cloudflare limits, CPU/subrequest/storage operations, consistency/availability and account-specific plan in the region/date of execution. Avoid hardcoded pricing or made-up user-count thresholds. If an operation times out after an external mutation, verify idempotency and reconcile state before repeating.

## Release/fault tests
- Wrong binding/resource must fail without granting extra permissions.
- Unauthorized/anonymous access must be rejected at intended boundary.
- Duplicate write, content size, pagination/query limits and network/proxy errors must be handled.
- Verify preview secrets/routing isolation and protected admin URL on production.
- Rollback and data retention/deletion tested in a dedicated environment.

## Official docs
- https://developers.cloudflare.com/d1/worker-api/
- https://developers.cloudflare.com/d1/worker-api/prepared-statements/
