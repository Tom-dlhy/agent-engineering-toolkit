# Databricks Bundles — direct engine, state migration and rollback

Read when: an existing bundle deployed with Terraform-backed state is moved to the GA direct deployment engine, changing bundle identity or recovering failed deployment.

## Why this is dangerous
A bundle manages a set of workspace resources and state, not only YAML source files. Changing bundle name/root/target, principal, engine or workspace can make resources appear missing and prompt duplicate creation or destructive replacement. Existing bundle identities may be deployed from local or workspace contexts but still refer to the same resources when configuration matches.

Databricks introduced a migration path from Terraform to direct deployment engine; the direct engine became GA with CLI 1.3.0 (Jun 2026) and defaults for **new** bundles. Don't assume upgrading the CLI transparently migrates existing state. Confirm exact current CLI commands and migration support with official docs before acting.

## Safe state transition ledger
~~~text
OLD: CLI version, engine, bundle root/name, environment/target
WORKSPACE: exact URL, deployed identity, owner service principal
RESOURCE INVENTORY: job IDs, pipeline IDs, catalog/schema dependencies
DRIFT: actual workspace resources versus last stored bundle state
NEW: CLI/engine version, planned changes and state migration steps
RISK: create/replace/delete, schedule, job state, artifact/version drift
BACKUP: old state/manifest, prior deployment revision and data output snapshot
AUTHORIZATION: change owner + reviewed plan / staging rehearsal
POSTCHECK: same intended resource identity, correct jobs/data/access
~~~

Before applying a migration, ensure an actual recovery mechanism for deleted/changed resources and that side effects on downstream data can be reconciled. Do not call bundle destroy to “reset stuck state”: this can remove live jobs/pipelines and complicate replay.

## Rollback reality
A git revert of YAML isn't always enough to roll back target state, database contents, checkpoint offsets or new table features. Keep a previous deployable bundle revision and verify restoring it will not violate source/target compatibility. If irreversible schema/data changes were deployed, prepare forward-fix/restore strategy with operational and data owner approval.

Tests: wrong target workspace, changed bundle identity, deleted resource in drift, unknown provider grants, incompatible migration, partial job deployment, stopped pipeline and excessive cost after rollback. Label unexecuted recovery steps UNRUN.

Sources: https://docs.databricks.com/aws/en/release-notes/dev-tools/bundles and https://docs.databricks.com/aws/en/dev-tools/bundles/ and https://docs.databricks.com/aws/en/dev-tools/bundles/faqs
