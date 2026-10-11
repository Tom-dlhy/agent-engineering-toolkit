# Governed-tag ABAC, row filters, masks and effective denied access

Read when: designing tenant/location segregation, confidential column masking, centralized data classification policy or evaluating UC ABAC support.

## Choose policy level
Databricks recommends **ABAC with governed tags** for centrally managed cross-table filtering/masking when supported; table-specific row filters/column masks can handle localized cases. ABAC also defines additional grant/deny policy concepts (some Beta as of Sep 2026); distinguish preview features and version gates.

Runtime requirements for ABAC row/mask include serverless or Standard DBR 16.4+; Dedicated compute requires compatible version and fine-grained access control configuration. Other environments must be tested, not assumed. Governed tags have controlled assignment rights; ungoverned descriptive tags are insufficient for ABAC protection.

## Fail-closed policy design
1. Define actor, tenant/region, resource and permitted columns/rows; explicit negative cases.
2. Decide trusted identity functions and governed-tag scope; avoid client-supplied tenant_id used as authorization.
3. Write UDF returning boolean for row filter or compatible type for column mask; preserve nullable/array/type semantics.
4. Define separation of duties for tag managers, policy owners, catalog owner and data producers.
5. Test tag propagation, policy precedence, views, joins and materialized/derived objects. Reclassifying a tag can change access across many objects.
6. Compare policy-protected query performance with allowed workload; complex UDF logic may add cost.
7. Approve rollout and validate with actual principals/compute mode before publication.

## Negative acceptance matrix
~~~text
A_READER: A rows allowed, B rows denied
B_READER: B rows allowed, A rows denied
UNAUTHORIZED: no direct underlying table/object privilege
PII_MASKED: masked email/phone, type-compatible
PII_APPROVED: unmasked only under exact authorized role
WRONG_WORKSPACE: denied even if analyst role otherwise permitted
UNTAGGED_NEW_TABLE: owner must classify before granting broad SELECT
~~~
These are **test expectations**, not proof a remote policy exists. Check unsupported compute and policy limitations before claiming the same outcome on every runtime. Avoid creating preview DENY grants without reviewing exact maturity and rollback.

Sources: https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/ and https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/core-concepts and https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/requirements and https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/
