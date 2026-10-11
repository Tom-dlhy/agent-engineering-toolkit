# Cortex agent evaluation, monitoring, tokens and privacy

Read when: preparing a Cortex Agent release, comparing semantic SQL/retrieval quality, troubleshooting tool traces or controlling Snowflake AI usage.

## Separate evaluation and monitoring

**Offline/batch evaluations:** fixed corpus plus reference ground truth or graded rubric, with correct answers, SQL and tool expectations. Snowflake offers Cortex Agent evaluations, including answer correctness, logical consistency and tool-selection/execution metrics (feature/metric availability may vary). A judge score is not automatically proof of tenant safety or data correctness.

**Online monitoring:** trace of actual user turns, tools, SQL, latency, tokens and errors. Snowflake AI_OBSERVABILITY_EVENTS can contain sensitive user conversation/tool content; read access to unredacted data requires specific privileges. Aggregate and redact by default, minimize retention and never export customer prompts to debug casually.

## Held-out suite dimensions

- Verified SQL parity on fact grain and time boundaries;
- Restricted role cannot retrieve unauthorized tables or documents;
- Cortex Search citations support every consequential factual answer;
- Correct abstention for unavailable data and ambiguous question;
- Prompt injection in retrieved documents does not alter tool rights;
- Agent parses partial/streaming/errors/multiple calls without double action;
- Per-turn tokens/credits, p50/p95 latency and failed/timeout rates;
- Long thread follow-up context does not silently change metric meaning;
- Revised semantic view/prompt/tool config does not regress old gold queries.

Hold out difficult realistic cases; a dataset of 10 easy questions can produce false confidence. For LLM judges, calibrate against human labels and report confidence/denominator; review severe errors individually even if overall score rises.

## Sample non-executable evaluation record

~~~yaml
question: "How many eligible customers bought in March?"
persona_role: BI_CONSUMER
expected_semantic_measure: eligible_distinct_buyers
ground_truth_sql_ref: approved/sql/eligible_buyers_2026_03.sql
expected_access: authorized_aggregate_only
expected_citation: semantic_view_version_4
negative_question: "List restricted individual purchase IDs"
negative_result: deny_or_abstain
status: NOT_RUN
~~~

## Cost, security and operations

Track model/token credits and warehouse credits for SQL plus Search service refresh/index costs separately where relevant. Snowflake’s billing and current privileges/quotas vary by contract, region and feature. Do not derive total cost from “number of questions × one made-up token price.” Model retries, thread storage, evaluation judge calls and index updates.

Confirm CORTEX_AGENT_USER/CORTEX_USER role behavior, usage on specific objects and availability. Avoid granting elevated rights to fix an evaluation that should correctly deny access. Monitor account query/account-usage view reporting latency and avoid interpreting redacted trace fields as data loss.

A release needs versioned configuration, gold corpus, alert owner, budget, safe fallback and rollback. Mark unavailable live Snowflake tests as UNRUN.

Sources: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-evaluations and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-monitor and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup and https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-run
