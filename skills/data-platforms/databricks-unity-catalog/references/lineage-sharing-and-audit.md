# Unity Catalog lineage, external data sharing and change audit

Read when: evaluating dataset/model lineage, releasing data to external consumers, checking governance drift or restoring access after role/policy change.

## Lineage and data disclosure
Identify publisher, data owner, producer, transform, consumer, workspace, external location, share, model and public artifact. UC lineage can show table/column dependencies when supported, but **absence of an edge** may reflect unobserved operations or inaccessible lineage, not proof a dataset is unused.

Delta Sharing and cross-workspace/catalog bindings are different controls. A share/listing exposing a governed view outside organization boundaries is a new external data release, requiring owner contract, privacy/residency and revocation review.

## Practical audit
Record actual object owner, grants, workspace bindings, governed tags and policies, external location and storage credential ACL. Inspect available system tables/audit logs and their visibility/latency under approved identities. Configuration diffs should include changes to:
- GRANT/REVOKE, ownership and inherited access;
- ABAC policies and tag attachments;
- managed/external storage path, location, volume;
- external shares and recipients;
- models, functions, UDFs and derived materializations;
- service principal permissions and workspace access.

Do not dump protected SQL/query text, credentials or raw customer records into incident logs. Separate security controls (what is allowed) from legal basis (whether use should occur).

## Change-control packet
~~~text
TARGET: catalog.schema.object, workspace, principal and consumer
BASELINE: inspected effective grants, tags, lineage and dependencies
CHANGE: exact grant/policy/share proposal (not applied)
NEGATIVE: unauthorized role, workspace and shared-consumer cases
RISK: outage, newly visible PII, data export, revoked service access
ROLLBACK: restore policy/grant and validate no open-access interval
APPROVAL: identity of authorized owner and scheduled change window
POSTCHECK: actual access under consuming roles, audit/lineage update
~~~

Do not infer effective permissions from one admin session or a UI screenshot. No production share, storage mutation or grant change without permission.

Sources: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/ and https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage and https://docs.databricks.com/aws/en/delta-sharing/
