---
name: databricks-automation-bundles
domain: data-platforms
version: "1.0.0"
description: >-
  Use when structuring and promoting Databricks Declarative Automation Bundles, databricks.yml resources, environment targets, CI/CD, CLI validation, deployment state or rollback. Do not use for general Terraform infrastructure planning, a lone notebook change or unauthorized production deployment.
---

# Databricks Declarative Automation Bundles — source-controlled assets with deployment state

## Mission and naming

Use **Declarative Automation Bundles** (formerly Databricks Asset Bundles) to package reviewed Databricks resources, Python sources, jobs, pipelines, models and deployment configurations. The rename is nonbreaking: the **databricks bundle** CLI and YAML conventions remain. Do not confuse bundle resource deployment with infrastructure Terraform workflows or CI proof of actual pipeline data correctness.

## Compatibility and identity inventory

1. Record CLI version, target cloud/account/workspace, authentication method, user/service principal, existing bundle state identity, deployment engine and resource types. New bundles with CLI 1.3.0+ use the GA **direct deployment engine** by default; existing Terraform-backed bundle state may require explicit migration.
2. Bundle root has **one databricks.yml** with bundle name and target config; use included resource files and validated variables for larger projects, no secrets in YAML.
3. Define dev/staging/prod targets with explicit workspace paths, catalog/schema names, run-as identity, allowed compute, environment-specific variables, permissions and budget. Ensure targets cannot accidentally reference production datasets from dev.
4. Identify current resource ownership and state: deploying under a changed root path, identity or bundle target can create duplicate jobs, orphan former assets or overwrite wrong pipelines.
5. Use fixed artifacts/dependency versions and CI source SHA. Plan/do validation before deployment; **bundle validate** is syntax/configuration evidence, not an executed job.
6. Use **bundle plan** only where CLI/version/engine supports it, examine resource diff; select-only planning/deploy switches have documented limitations and shouldn't be used casually in production.
7. Dev integration tests -> human-reviewed staging/prod promotion -> observability and rollback. Production **bundle deploy**, state migrate or **bundle destroy** requires explicit approval.

## Procedure

~~~text
SOURCE COMMIT + PINNED DEPENDENCIES
 -> OFFLINE TESTS AND YAML POLICY CHECKS
 -> CLI VALIDATE (workspace identity verified)
 -> PLAN AND INSPECT RESOURCE CHANGES
 -> AUTHORIZED DEV DEPLOY + PIPELINE/ACL TEST
 -> REVIEWED ARTIFACT AND OWNER APPROVAL
 -> STAGING/PROD DEPLOY + VERSIONED AUDIT
 -> OBSERVE, RECONCILE AND ROLLBACK
~~~

A deployment that exits 0 can still have wrong dataset outputs or broadened permissions. Validate job identity, data publication, secrets, quotas, schedule overlap and rollback as independent gates. Never silently “fix” a production drift by destroying resource state.

## Targeted references

- [Bundle configuration, CLI and target contracts](references/bundle-config-and-targets.md) — **read when** authoring YAML, variables, includes or resource graph.
- [CI/CD, approvals and service principal identity](references/ci-cd-and-service-principals.md) — **read when** promoting artifacts safely through environments.
- [Deployment engines, ownership and recovery](references/deployment-state-and-recovery.md) — **read when** migrating older state or debugging resource collision.

## Boundary and exit

cloud/terraform owns general external infrastructure; databricks-lakeflow-pipelines owns CDC/data logic; quality/release-readiness owns universal launch governance. This skill owns **Databricks deployment configuration, CLI semantics and state-safe promotion**.

Return a reviewable manifest and dry-run plan, actual target identity/permissions, pinned CLI and dependency versions, test/rollback matrix, migration impact and owner approvals. If no workspace access, mark CLI or live deploy checks UNRUN; never pretend validation or jobs ran.
