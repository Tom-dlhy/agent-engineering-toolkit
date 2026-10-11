# Roles, grants and ownership in Snowflake

Read when: building role hierarchy, least privilege, managed access schema or a consumer service role.

## Distinguish all layers

Snowflake **account roles** and **database roles** are not cloud IAM roles. Database roles are granted to account roles rather than activated directly in a user session. Roles inherit granted child-role privileges through hierarchy. An object owner has OWNERSHIP, but in a **managed access schema** the schema owner or a role with MANAGE GRANTS controls grants on child objects, even when someone else owns a child.

A read query often needs database and schema USAGE, table/view SELECT, and warehouse USAGE. Permissions are operation-specific; don't treat SQL role assignment as AWS cloud credentials. Avoid giving a BI job ACCOUNTADMIN to bypass a denied query.

## Design an authorization graph

- Access roles: grant narrowly scoped object SELECT/INSERT/UPDATE by business responsibility.
- Functional roles: aggregate the minimum access roles needed for a job.
- Service roles: isolate ELT jobs, models/agents, CI and humans.
- Schema ownership: define policy and grant operators; controlled break-glass with audit.
- Future grants: apply only to **new** objects, while ALL TABLES covers existing ones. Schema-level future grants can override database-level grants of same object type; verify actual precedence.
- Clones, database roles, policy objects and object ownership transfer may not carry permissions as expected; test target objects.

Illustrative **proposed-only** SQL, never apply to an actual account without owner approval:

~~~sql
GRANT USAGE ON WAREHOUSE ANALYTICS_WH TO ROLE REPORT_READER;
GRANT USAGE ON DATABASE DEV_DB TO ROLE REPORT_READER;
GRANT USAGE ON SCHEMA DEV_DB.MART TO ROLE REPORT_READER;
GRANT SELECT ON ALL TABLES IN SCHEMA DEV_DB.MART TO ROLE REPORT_READER;
-- Future objects need a distinct approved rule if desired:
-- GRANT SELECT ON FUTURE TABLES IN SCHEMA DEV_DB.MART TO ROLE REPORT_READER;
~~~

Review whether all existing tables are appropriate for this role: a broad schema-level SELECT may expose restricted material. Narrow table/view grants are often safer.

## Negative tests

Use actual permitted test role sessions (never privileged owner as proxy):
1. Authorized analyst can read approved view and not write it.
2. Unrelated role cannot select underlying private base tables/stages.
3. New tables do not inherit unexpected future grants.
4. Managed access object owner cannot silently grant access if not schema owner.
5. ELT service can use only required warehouse, stage, table and task.
6. Application uses no permanent privileged admin login.

A text review of GRANT statements is not proof the session uses the expected active/inherited roles. Record role used, exact expected denial, actual result and corrective owner.

Sources: https://docs.snowflake.com/en/user-guide/security-access-control-overview and https://docs.snowflake.com/en/user-guide/security-access-control-configure and https://docs.snowflake.com/en/user-guide/security-access-control-considerations
