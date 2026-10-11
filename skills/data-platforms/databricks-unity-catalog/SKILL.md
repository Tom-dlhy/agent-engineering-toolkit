---
name: databricks-unity-catalog
domain: data-platforms
version: "1.0.0"
description: >-
  Use when designing Databricks Unity Catalog securable grants, catalog/schema access, managed/external storage, workspace bindings, ABAC, row filters, column masks, lineage or Delta Sharing. Do not use for AWS IAM alone, Snowflake grants, GDPR legal signoff or Unity Gateway runtime LLM traffic policies.
---

# Databricks Unity Catalog — enforce asset-level privileges and policy

## Mission and context

Govern Databricks **data/AI assets** with least privilege, ownership and traceable metadata. Unity Catalog security is multi-layered: privileges/ownership, governed-tag ABAC, per-table row filters/column masks and workspace-level bindings. These complement rather than replace one another. Confirm cloud, metastore/workspace, compute access mode and Databricks Runtime before proposing policies; a model with correct SQL grants but wrong workspace/storage permissions still fails.

## Access-control decision process

1. Identify users, groups, service principals, automated jobs, model-serving identities and third-party consumers. Record actual data classifications and allowed/denied actions.
2. Map metastore, catalog, schema, table/view/volume/function/model, external location/storage credential and workspace binding. Separate managed from external objects and cloud IAM.
3. Build minimal privilege matrix; inherited catalog/schema rights, ownership and privileges on supporting objects matter. Never give account admin or broad file access merely to unblock SELECT.
4. For rules across many objects, evaluate **ABAC governed tags and policies** (Databricks' preferred centralized approach). For a few specific objects, use table row filters/column masks as appropriate. Confirm runtime requirements: ABAC row/mask policies may require serverless or DBR 16.4+, and governed tags must actually be governed; not all runtimes and policy types have identical availability.
5. Test principal-specific access through SQL, jobs, model APIs and external paths. A client-side WHERE tenant_id filter is not server authorization.
6. Inspect lineage for real upstream/downstream exposure; handle Delta Sharing/publication as an external data-release decision with legal/privacy owner where relevant.
7. Plan grant and policy migration with owner approvals, rollback and no temporary unrestricted access interval.

## Required negative checks

- Tenant A cannot read tenant B rows or unmask restricted PII.
- Job service principal cannot read unrelated catalog or external location.
- Workspace binding blocks unauthorized workspace access even if catalog is visible elsewhere.
- Governed tag change updates the intended policy scope without attaching to sensitive unintended tables.
- A model/feature asset exposed via serving does not bypass data rights assumed for analysts.
- Sharing export is reviewed as a separate consumer role/contract; no fabricated privacy clearance.

## References

- [UC grants, storage credentials and workspace boundaries](references/privileges-and-storage-boundaries.md) — **read when** mapping privileges and external data locations.
- [Governed-tag ABAC, row filters/masks and isolation tests](references/abac-row-masking-and-policy-tests.md) — **read when** defining fine-grained access.
- [Lineage, sharing, audit and controlled changes](references/lineage-sharing-and-audit.md) — **read when** disclosing data or checking policy drift.

## Boundaries and finish

Cloud IAM specialist handles storage-account roles; privacy-compliance-lead owns lawful processing; databricks-ai-governance governs inference **requests and tools**, databricks-mlflow-mlops owns model lifecycle. This skill handles **Unity Catalog assets and access**.

Produce resource/principal/policy graph, edition/runtime/compute gates, approved SQL proposal, explicit allow/deny fixtures, audit source and rollback. Mark all effective policies unverified unless actually tested in an authorized workspace. Never GRANT/REVOKE, create external locations or share data without approval.
