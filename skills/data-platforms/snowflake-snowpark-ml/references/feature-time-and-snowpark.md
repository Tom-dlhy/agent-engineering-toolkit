# Point-in-time ML features and safe Snowpark execution

Read when: building historical score observation tables, Snowpark feature transformations, Feature Store views or train/serve consistency.

## Define the prediction row before code

A scoring base with entity and observation timestamp must be a valid population at that historical date. Record entity identity and eligibility/opt-in, observation UTC, available feature cutoff, target horizon (future event), label maturity and late corrections. Distinguish event_time, ingestion_time and feature_available_at; a feature whose value became known after observation cannot be used, even if its event_ts is older.

A clear feature invariant: for each (entity, observation_date), select only a feature version **available to the scoring system at that observation**, with no post-outcome enrichment. Rolling-window aggregates must end at observation_time. Use temporal holdouts and avoid splitting identical entities/monthly snapshots randomly when that leaks future correlations.

Safe conceptual SQL for a synthetic, already prepared history (adapt real schema):

~~~sql
WITH candidates AS (
  SELECT o.CODE_INDIVIDU, o.OBS_DATE,
         f.FEATURE_VALUE, f.AVAILABLE_AT,
         ROW_NUMBER() OVER (
           PARTITION BY o.CODE_INDIVIDU, o.OBS_DATE
           ORDER BY f.AVAILABLE_AT DESC, f.SOURCE_VERSION DESC
         ) AS RN
  FROM DEV_DB.ML.OBSERVATIONS o
  LEFT JOIN DEV_DB.ML.FEATURE_HISTORY f
    ON f.CODE_INDIVIDU = o.CODE_INDIVIDU
   AND f.AVAILABLE_AT <= o.OBS_DATE
)
SELECT CODE_INDIVIDU, OBS_DATE, FEATURE_VALUE
FROM candidates WHERE RN = 1;
~~~

This is illustrative; if OBS_DATE is date rather than timestamp, define cutoff timezone/end-of-day correctly. In real history, multi-feature records may need separate as-of joins; a single row_number across mixed sources can silently drop valid features. Tie-breakers must be stable; not all Snowflake primary-key constraints enforce uniqueness in standard tables.

## Snowpark execution discipline

Snowpark DataFrames are lazily constructed; actions materialize execution. Keep transformations in Snowflake where feasible and verify generated SQL and warehouse/query plans. Avoid collecting all rows into Python driver memory, leaking sensitive examples through to_pandas, and forcing UDFs for simple SQL operations. Confirm Python package/warehouse permissions and runtime before registering functions.

Snowflake Feature Store: Enterprise Edition may be required; an Entity identifies join keys, FeatureView defines feature computation and refresh; managed feature views can use dynamic tables, external feature views have externally maintained data. Current APIs support timestamp-column semantics and point-in-time dataset methods; verify exact snowflake-ml-python version for append-only historical snapshots before using them. Refreshing a managed view does **not** retroactively create correct historical values unless source history exists.

## Leakage test matrix

| Scenario | Expected |
|---|---|
| Post-outcome feature update | Must not change prior observation training features |
| Same entity in adjacent months | Temporal validation windows don't overlap target horizon |
| Duplicate observation key | Deterministic dedupe or error; no accidental fanout |
| Feature missing at cutoff | Explicit null/default and missingness trace |
| Backdated source event ingested late | Respect available_at, not just event time |
| Entity removed from eligible population | Respect historical eligibility and privacy requirements |

Handoff to data-pipeline-quality for broad source validation; this skill owns Snowflake feature operations and ML leakage controls.

Sources: https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-views and https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering and https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes
