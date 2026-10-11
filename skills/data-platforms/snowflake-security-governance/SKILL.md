---
name: snowflake-security-governance
domain: data-platforms
version: "1.0.0"
description: >-
  Use when auditing or designing Snowflake roles, grants, managed-access schemas, row access/masking policies, data sharing and account audit controls. Do not use for generic AWS/GCP IAM, GDPR legal conclusions or casually issuing ACCOUNTADMIN-wide grants for one SQL query.
---

# Snowflake security governance — prove privileges at the consuming role

## Mission

Protect Snowflake objects, sensitive data and operations using **least privilege, separation of duties, contextual row/column protection and auditable change controls**. Distinguish account roles, database roles, inherited privileges, ownership, schema-level authority, policy application privileges and how the **actual consuming role** accesses data. Documentation of a policy is not proof that access is restricted in real sessions.

## Security decision method

1. Map principals and paths: service users, human analysts, model-serving roles, tools/agents, shares/consumers, CI automation and break-glass administration. Record target account edition, region, object locations and current role hierarchy.
2. Construct grant matrix from intended operations (USAGE on warehouse/database/schema, SELECT/DML on exact objects, CREATE only where necessary). Examine future grants and ownership; avoid broad PUBLIC/ACCOUNTADMIN shortcuts.
3. For managed access schemas, verify who is authorized to grant on child objects. The ability to create an object and the ability to grant others its use can differ.
4. Need **row-level rules**? Evaluate ROW ACCESS POLICY edition/permissions, mapping tables, role context and query-plan cost; test protected joins/views, role inheritance and denied tenants. Never claim generic SQL WHERE predicates equal platform-enforced RLS.
5. Need column protection? Define MASKING POLICY for sensitive fields and verify expression types/role logic, masked/unmasked outputs, dependent views and audit. Masking policies and row access policies are separate mechanisms; their combination has ordering and compatibility consequences.
6. Separate ownership/control from data visibility: powerful administrative role must not automatically mean unrestricted analyst query access. Build separation of duty where supported, plus documented exception process.
7. Protect data movement: shares/listings, data unloads, COPY, stages, integrations, cross-region replication and ML/AI inference traces. Privacy/legal authority determines whether each processing/transfer is permissible.
8. Audit changes with permitted ACCOUNT_USAGE/INFORMATION_SCHEMA/Snowsight resources, acknowledging reporting latency and visibility. Establish authorized role-change rollout, negative tests, backout and credential rotation boundaries.

## Reference router

- [Role hierarchy, database roles, future grants, SoD](references/roles-grants-and-ownership.md) — **read when** designing RBAC, managed schemas or access grants.
- [Row access, masking and negative authorization tests](references/row-masking-and-access-policies.md) — **read when** enforcing tenant or sensitive-column access.
- [Sharing, audit, identity and production change review](references/sharing-audit-and-change-control.md) — **read when** managing external access, data release or investigating grants.

## Explicit boundaries

cloud/aws-iam-security and gcp-iam-identity govern cloud principals; personas/privacy-compliance-lead prepares lawful/privacy decisions but doesn't author Snowflake policies; ai/agent-tool-safety sets generic agent action controls. This skill owns **Snowflake SQL-level and platform governance**. Never run GRANT, REVOKE, CREATE/ALTER POLICY, DROP, key rotation or public share configuration without owner authorization.

## Deliverable

Provide principal/object/privilege graph, edition-qualified policy eligibility, DDL as a **proposal unless approved**, negative read/write test matrix, audit source and expected delays, migration impact, rollback and explicitly assigned approver. If actual Snowflake account is not connected, mark all deployed-state claims UNVERIFIED.
