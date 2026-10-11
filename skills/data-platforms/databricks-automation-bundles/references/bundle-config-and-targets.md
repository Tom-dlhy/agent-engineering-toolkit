# Declarative Automation Bundles — configuration, source layout and target isolation

Read when: authoring Databricks YAML resources, include files, environment targets and variable overrides for versioned deployments.

## Bundle identity and CLI
A bundle root contains one databricks.yml. Organize resource YAML and Python/notebook sources via supported includes. As of Mar 2026, “Asset Bundles” is renamed **Declarative Automation Bundles**, and the CLI remains **databricks bundle**. CLI 1.3.0+ new projects default to GA direct deployment engine; existing bundle state may use the old engine. Pin CLI versions in CI rather than trusting what exists on a developer laptop.

Illustrative config, **not yet validated in a workspace**:
~~~yaml
bundle:
  name: demo-data-pipeline
include:
  - resources/*.yml
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://example-workspace.cloud.databricks.com
  prod:
    mode: production
    workspace:
      host: https://prod-placeholder.cloud.databricks.com
~~~
Both URLs are placeholders, never credentials. Confirm exact workspace cloud/identity, target-supported settings and current CLI config contract before use. Production target must have separate run-as principal, paths/catalog and approval gate; never rely on changing only display name.

## Safe validation sequence
1. Inspect root YAML syntax, includes, variables, resource dependencies and environment overrides.
2. Verify target resource names/state identity, scripts/notebooks actually present, package pinning and dataset namespaces.
3. Check secret references only, never literal PAT/client secret/password in YAML.
4. Run offline unit tests, then **bundle validate -t dev** against authorized host/auth where necessary.
5. Use plan/diff when supported and inspect the exact resources that would change. Validation isn't deployment.
6. Only use bundle deploy in permitted workspace and after quality/approval. Keep the same reviewed commit for promotion.

## Negative QA
Missing include file, wrong variable/namespace, prod endpoint in dev target, duplicate job resource ID, unsupported CLI feature, plain-text credential, service principal without grant, stale state from another bundle. Fail closed and report exact target paths.

Sources: https://docs.databricks.com/aws/en/dev-tools/bundles/ and https://docs.databricks.com/aws/en/dev-tools/bundles/settings and https://docs.databricks.com/aws/en/release-notes/dev-tools/bundles
