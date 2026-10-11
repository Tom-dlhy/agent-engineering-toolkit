# Row access, dynamic masking and verified negative access

Read when: deploying row isolation, sensitive-column masking, tenant entitlements or policy/role validation in Snowflake.

## Platform mechanisms and edition gate

ROW ACCESS POLICY limits rows visible when querying a protected table/view; MASKING POLICY changes protected column values based on role/context. They are not interchangeable, and neither simply follows a client-supplied WHERE clause. Snowflake documents Enterprise Edition requirements for row access and dynamic masking; check actual edition and data policy constraints before designing DDL.

Context functions matter: CURRENT_ROLE shows active role; IS_ROLE_IN_SESSION captures inherited account-role context; IS_DATABASE_ROLE_IN_SESSION is relevant for database-role based entitlements; INVOKER_ROLE may differ in views/procedures. A secured mapping table needs its own ownership/readability and careful policy evaluation.

## Implementation sequence

1. State actor/tenant/resource matrix, including exceptions and masking expectations.
2. Choose trusted entitlement source; refuse unverified client-provided tenant IDs as authorization.
3. Separate data owner, policy owner and deployment operator in least privilege design.
4. Draft policy and attach in sandbox only with approved APPLY privileges. Test wrong tenant/role and role inheritance, including secondary roles where relevant.
5. Verify policy-dependent JOIN/view results, NULLs, type constraints, query performance and policy application order.
6. Audit POLICY_REFERENCES for where a policy is attached; SHOW POLICY does not imply enforcement on all intended objects.
7. Treat materialized views, streams, cross-account shares and derived assets as distinct tests, not assumptions about policy propagation.
8. Migrate in a safe order to avoid an interval where private rows are unexpectedly visible.

## Negative fixture

~~~text
TENANT_A_READER -> rows for A visible, B rows hidden
TENANT_B_READER -> rows for B visible, A rows hidden
NO_ACCESS_ROLE  -> direct base table SELECT denied
ANALYST_ROLE    -> permitted rows, PII columns masked
PII_APPROVED    -> permitted rows, protected columns unmasked by policy
OBJECT_CREATOR  -> cannot grant broader access in managed-access schema
~~~

These are **expected test cases**, not evidence any role was exercised. Inspect actual role session under authorized test account; count denied and returned records, including joins, NULLs and stale access. Some contexts are unsupported (e.g. policy cannot be attached directly to stream); consult current official documentation.

If Enterprise features are unavailable, consider role-limited secure views and strict base-table grants, but never assert they are automatically equivalent to row-policy enforcement. Escalate to platform security owner.

Sources: https://docs.snowflake.com/en/user-guide/security-row-intro and https://docs.snowflake.com/en/user-guide/security-column-ddm-intro and https://docs.snowflake.com/en/user-guide/security-column-advanced
