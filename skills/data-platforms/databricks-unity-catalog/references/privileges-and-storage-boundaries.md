# Unity Catalog privileges, parent scopes, storage and workspace bindings

Read when: troubleshooting a UC access denial or designing least-privilege access to managed/external data and models.

## Map the exact path
Workspace/cloud/metastore → principal/group/service principal → catalog → schema → securable (table, view, volume, function, model) → underlying data location/compute. UC object privileges are not the same as external cloud role policies. Storage credentials define authentication to cloud stores; external locations scope cloud paths/managed storage access. Avoid giving storage IAM keys to application code.

Record object ownership and parent privileges. USE CATALOG/USE SCHEMA can be necessary even with downstream SELECT. Workspace-catalog bindings can independently limit accessible catalogs, external locations and storage credentials. A principal with correct SQL grant in one workspace may still be denied in another.

## Illustrative proposal only (do not execute automatically)
~~~sql
-- Run only after authority and actual catalog/schema are verified.
GRANT USE CATALOG ON CATALOG dev_catalog TO analysts;
GRANT USE SCHEMA ON SCHEMA dev_catalog.analytics TO analysts;
GRANT SELECT ON TABLE dev_catalog.analytics.orders TO analysts;
~~~
Confirm target object classifications and scope; different object types, external locations and functions require different privileges. Do not use account admin to “fix” an analyst query. Test service-principal access independently from human access.

## Decision and tests
1. Choose managed table vs external storage and identify actual owner and approved region.
2. Design one privilege matrix for expected read/write, schema mutation, model use, and export.
3. Test direct SELECT, joining protected objects, READ VOLUME path, and view/function execution under authorized role.
4. Test forbidden cross-workspace/catalog access and stale service-principal grants.
5. Review inheriting/owner grants after ownership transfer and after clone, not just before.
6. Coordinate Unity Gateway for model **runtime requests**, but UC asset/model privileges must still be correct.
7. Route lawful processing/cross-border rules to privacy owner; passing UC checks is not a legal authorization.

Do not GRANT/REVOKE, create storage credential, attach workspace binding or transfer ownership without explicit approval and rollback.

Sources: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/ and https://docs.databricks.com/aws/en/data-governance/unity-catalog/ and https://docs.databricks.com/aws/en/connect/unity-catalog/
