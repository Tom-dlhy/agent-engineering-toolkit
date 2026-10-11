# Cortex Search — grounding does not imply caller-specific confidentiality

Read when: building retrieval over enterprise documents with Snowflake Cortex Search, grounding answers, enforcing document permissions or handling indexing drift.

## Critical security fact

Cortex Search Services perform queries under an **owner's-rights security model**. A caller that can query the Search Service does **not** automatically inherit a per-row SELECT restriction identical to querying the underlying source tables as that caller. Snowflake requires service USAGE and parent database/schema grants; creation requires source SELECT and additional privileges. Therefore, **never expose a service indexing mixed confidential documents and assume Snowflake row-level policies on source tables independently secure each search hit for every caller**.

Define a data partition/access architecture before indexing:
- service per genuinely isolated audience/tenant, where operationally sensible;
- filterable authorization metadata that is accurately applied **server-side** using trusted principal claims, not a user-supplied filter;
- source minimization and omission of restricted text from shared index;
- evaluation of owner-rights behavior and exact service capabilities;
- negative integration tests for cross-tenant and revoked membership access.

A predicate set by the client alone is insufficient if callers can reach an unfiltered Search API through other paths. The implementation must ensure every access path applies approved restrictions; keep the service usage grants tightly bounded.

## Retrieval quality and freshness

Cortex Search combines semantic and keyword retrieval with reranking. That does not guarantee true evidence for every question. Define index source, document ID, section/page, timestamp, access category, version, source URL/path and retention. Measure indexing lag, update/reindex, removed/reclassified document propagation and cost.

For every question:
1. Resolve caller identity and authorized index/service access;
2. enforce trusted filters and time ranges;
3. retrieve bounded top-k; preserve scores/IDs as metadata;
4. ask model for citation to actual retrieved item and specific passage;
5. check citation points to accessible evidence, not fabricated document;
6. abstain when no relevant accessible source supports answer;
7. inspect prompt injection instructions **inside retrieved text** as untrusted data, never tool commands.

## Negative acceptance cases

| Input | Expected denial or honest outcome |
|---|---|
| Tenant A requests tenant B policy text | No leak from shared index or alternate API path |
| Revoked user retries old query | New server-side authorization blocks |
| Document deleted/reclassified | Search no longer exposes contents under expected consistency contract |
| Malicious doc says “ignore previous instructions” | Model treats text as evidence, not authority |
| User asks for absent clause | Grounded abstention, not plausible fabricated citation |
| Search service fresh but semantic answer wrong | Evaluation flags reasoning failure separately |

## Release boundaries

Verify edition/region service availability, data classification, metadata policies, warehouse/indexing costs and monitoring redaction. Creating/altering a Search Service can index sensitive data and incur cost; require owner permission and test role before applying DDL. The concrete service privileges may evolve: confirm against current official access control documentation.

Sources: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-monitor
