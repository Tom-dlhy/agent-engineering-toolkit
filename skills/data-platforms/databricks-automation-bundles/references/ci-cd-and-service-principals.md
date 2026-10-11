# Databricks bundle CI/CD, principal identity and release gates

Read when: promoting a bundle through dev/staging/prod, configuring CI credentials or verifying safe target-specific permissions.

## Build ≠ deploy
Define the source commit, locked CLI/build dependency versions, tests, target workspace, service principal, job run-as identity, UC grants and shared asset ownership. An environment variable holding an account PAT is a credential risk: prefer approved noninteractive federation/OAuth secret management, never echo tokens. Cloud-specific identities differ.

## Proposed CI pipeline
~~~text
PR:
 - parse YAML / check resource inclusions and forbidden secrets
 - unit and deterministic contract tests for notebook/Python logic
 - lint/typecheck where meaningful
 - compile/validate pipeline SQL on fixtures when possible
 - inspect target references and resource identity drift
MERGE APPROVED:
 - pin immutable source artifact and Databricks CLI version
 - authorized bundle validate and plan on dev/staging
 - deploy to isolated dev, run data/ACL/freshness negative integration tests
 - human release approval and review plan for prod
 - prod deploy in allowed window
 - verify workload, data publication, grants, cost and rollback
~~~

Do not invent CI success if jobs weren't run. Separate deploy identity from data-processing principal: a CI operator permitted to create a job doesn't mean that job should execute as admin. Review service-principal permissions per resource; deny an automation role unnecessary DELETE, workspace root and external storage writes.

## Negative cases
- PR changes target to production workspace -> static policy gate BLOCK.
- One resource gets a new name, threatening creation/replacement -> plan/review required.
- Missing job principal grants -> fail without elevating to admin.
- Library dependencies differ between PR/dev/prod -> reject unpinned deployment.
- “bundle validate passed” but pipeline corrupts outputs -> dataset acceptance tests still required.
- Re-run CI under a different root/identity -> state and ownership must be reviewed.

Human approval for live bundle deploy, state migration/destroy and paid compute is non-negotiable. Return scoped CI evidence, resource identity, status and approved rollback—not a claim that source-control pipeline equals runtime correctness.

Sources: https://docs.databricks.com/aws/en/dev-tools/bundles/ and https://docs.databricks.com/aws/en/dev-tools/bundles/faqs and https://docs.databricks.com/aws/en/dev-tools/bundles/settings
