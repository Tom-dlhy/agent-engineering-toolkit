# Analytic fact grain, SCD2 and weighted measures

Run pure SQL tests using standard-library in-memory SQLite:

~~~bash
python -m unittest discover -s tests -p 'test_data_analytics_contract.py' -v
~~~

Covers grain uniqueness, historical half-open effective-date join,
double-count detection, SCD2 interval conflict, and weighted conversion
rate. This models semantic mistakes applicable across warehouses,
**not** Snowflake/dbt/BigQuery dialect compatibility, null/locking
semantics, partition costs or production-scale performance. A real
project must also execute tests on its pinned analytical engine.
