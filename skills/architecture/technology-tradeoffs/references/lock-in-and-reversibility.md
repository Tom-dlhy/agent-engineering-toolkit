# Provider lock-in, portability and evolution trade-offs

**Read when:** selecting a managed DB, cloud runtime, UI framework
or cross-provider SDK abstraction where exit/migration matters.

## Portability is a business requirement, not an automatic virtue

A native SDK may expose streaming/tooling/security capabilities
that a generic wrapper loses or normalizes incorrectly.
A portable interface can reduce future migration cost when
there is a real likelihood of switching and its semantics
are stable. Too many abstract interfaces add maintenance
and may hide provider-specific failure classes.

## Exit-plan checklist

- Identify proprietary APIs, data formats, credentials,
  regional entitlements, egress cost and retention constraints.
- Inventory exported data and whether export/import format
  preserves constraints, indexes, documents and versions.
- Use migration dry-run or dual-read/dual-write with careful
  ordering, auditing and rollback if required.
- Define acceptable outage, RTO/RPO, schema compatibility and
  alternative region/provider identity.
- Evaluate secrets and tenancy mappings across providers,
  plus data handling policy on any fallback.
- Decommission old resources only after retention/security
  signoff and actual traffic/consumer verification.

## Case: PostgreSQL cloud provider

PostgreSQL protocol compatibility does not imply identical
managed capabilities: extension support, connection limits,
replication, backup retention, pooling and region policies
may differ. Prove required extensions, maintenance windows,
restore test and cost. A cloud provider's export feature
may not transfer every operational control automatically.

## Case: LLM routing

LiteLLM can unify common request shapes but Bedrock, Vertex
and Azure differ in model capabilities, IAM, content/safety
blocks, quotas and response parts. A fallback may send data
to a nonapproved location or a model with different quality.
Portability requires explicit capability and privacy policy,
not only a common method name.

## Exit evidence

A realistic second implementation/spike, source+target
data/API compatibility tests, cost and migration plan,
and a decision trigger for leaving. Never promise zero
vendor lock-in or one-day cloud migration without proof.

Sources:
https://learn.microsoft.com/en-us/azure/architecture/guide/ ,
https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html .
