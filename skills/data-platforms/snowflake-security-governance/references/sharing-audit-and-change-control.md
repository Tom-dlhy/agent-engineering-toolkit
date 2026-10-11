# Snowflake sharing, audit and privileged change control

Read when: sharing data across Snowflake accounts, investigating access drift, reviewing role/policy DDL or controlling external data publication.

## Sharing is data release, not just another SELECT

Identify provider, consumer, objects and columns, purpose, controller and contractual/legal reviewer, region/cloud boundaries, access policies and revocation path. Secure Data Sharing, listings, replication and cross-cloud fulfillment have different rules. Do not equate “Snowflake hosted in EU” with freedom to share identifiable data elsewhere. Review actual consumer visibility, supported secure views, masking/row policies and compliance with the appropriate authority.

## Audit inventory

- account/database roles, ownership changes and inheritance;
- ALL versus FUTURE grants, managed access schema;
- CREATE/ALTER/DROP/ATTACH row/masking policies and mapped objects;
- service users, delegated access, network policies and integrations;
- stage COPY/unloads and account shares/listings;
- model/agent/Search service query access, trace visibility and export.

Use available Snowsight, INFORMATION_SCHEMA and SNOWFLAKE.ACCOUNT_USAGE views, respecting their latency and role requirements. POLICY_REFERENCES helps find attachments. Query text and unredacted Cortex logs may hold personal or confidential data, so restrict and minimize retention. Never publish secrets in a review log.

## Controlled authorization change

~~~text
REQUEST + owner/approval and reason
BASELINE: effective roles, grants, policy object and consumers
DIFF: exact SQL, edition requirements, blast radius, denied cases
SAFE DRY RUN: same object/role pattern in disposable schema
RECOVERY: restore privileges/policies without temporary exposure
EXECUTION: authorized operator and window; no silent DDL
POSTCHECK: role-specific allowed/denied queries and audit proof
~~~

A GRANT OWNERSHIP transfer, REVOKE, blanket GRANT or cross-region share can cut off dependent tasks or expose records. Need a rollback/communication plan before applying it. The existence of an Account Usage audit row is not proof the application still enforces tenant boundaries.

## Identity and transport

Authentication to the Snowflake account can use key-pair, OAuth and other supported methods, but session auth does not automatically give a data access right. Credentials belong in approved secret storage, not source code. Confirm service identity and active/secondary role, warehouse and object access; do not test using ACCOUNTADMIN in place of real consumer.

The privacy-compliance-lead persona owns legal purpose/transfer assessment; this skill only proposes platform-level security design and validation.

## Exit

Role/object/consumer graph, auditable change proposal, data-region check, security/privacy approvers, access test matrix with verified results or UNRUN, rollback and owner. Do not publish cross-account shares or rotate real keys without permission.

Sources: https://docs.snowflake.com/en/user-guide/secure-data-sharing-across-regions-platforms and https://docs.snowflake.com/en/user-guide/security-access-privileges-shares and https://docs.snowflake.com/en/user-guide/security-access-control-overview and https://docs.snowflake.com/en/user-guide/security-column-ddm-intro
