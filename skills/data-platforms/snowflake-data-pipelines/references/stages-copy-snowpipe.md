# Snowflake stages, COPY INTO and Snowpipe — file ingestion with a replay contract

Read when: loading staged files from S3/Azure/GCS, building Snowpipe notifications, tracing load history, or avoiding duplicate business rows.

## Select ingestion by source behavior

- COPY INTO uses a user-managed warehouse for scheduled/bulk loads and supports file format/validation controls.
- Snowpipe automates file-based micro-batch loading on event/REST notifications; it uses Snowflake-managed compute. It is not the same as Snowpipe Streaming (row ingestion APIs) and does not guarantee arrival order.
- A pipe's load metadata avoids some duplicate file loads, not application-level exactly-once semantics. Same-name changed files may not reload. Different filenames may contain duplicate business records.
- Snowpipe file load history and COPY file load history have distinct retention mechanisms and visibility; Snowflake explicitly cautions against using both for the same file collection.

## Preflight and implementation

1. Enumerate bucket/container, prefixes, file naming rules, immutable source version, producer retries, expected latency/size, data classifications and source schema.
2. Confirm storage integration credentials and Snowflake role privileges separately. Never embed account credentials in CREATE STAGE, examples, logs or git.
3. Define explicit FILE FORMAT (CSV quote/header/null or JSON/Parquet schema evolution), batch staging and quarantine policy. Keep METADATA$FILENAME and load time only if necessary and lawful.
4. Validate parser/columns on synthetic files in a disposable schema; compare source manifest count to row/business key reconciliation.
5. Load into an isolated raw layer, not directly into final user metrics. Deduplicate and handle late corrections by business key before publishing.
6. Set monitoring on notifications, last successful pipe ingest and missing source files. Document a backfill path distinct from live ingestion.

Optional read-only-ish preflight for supported COPY shapes (requires existing authorized stage/table/format):

~~~sql
-- VALIDATION_MODE checks files rather than publishing them.
COPY INTO DEV_DB.RAW.ORDERS
FROM @DEV_DB.RAW.ORDERS_STAGE
FILE_FORMAT = (FORMAT_NAME = 'DEV_DB.RAW.ORDERS_CSV')
VALIDATION_MODE = 'RETURN_ERRORS';
~~~

Validate command compatibility, column mapping and stage scope with current Snowflake docs; do not turn this into FORCE=TRUE or a production load without approval.

## Negative cases and operations

| Input | Expected result |
|---|---|
| Same notification twice | No unexpected duplicate load of that file; downstream keys still checked |
| Two files contain same order ID | Canonical key dedupe or explicit quarantine |
| Same path overwritten with new bytes | Manifest detects changed version, correction policy defined |
| File order changes | Output independent of staging order |
| Bad CSV delimiters / type coercion | Error/poison quarantine, not silent wrong types |
| Staging integration denied | Observable queue/backlog and reversible repair |
| Backfill while pipe running | Owner-approved conflict plan, no duplicate downstream row |

Return actual file manifest, error rows, reconciliation and versioned load policy. A successfully accepted file is not proof of final business correctness.

Sources: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro and https://docs.snowflake.com/en/sql-reference/sql/copy-into-table and https://docs.snowflake.com/en/user-guide/querying-metadata
