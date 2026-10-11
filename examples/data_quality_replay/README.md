# Data replay educational example (no DB/network)

This standard-library reducer models stable source revision,
deduplication, tenant scope and tombstone delete against replay.
Run from repo root:

~~~bash
python -m unittest discover -s tests -p 'test_data_replay_contract.py' -v
~~~

**Not production durability**: version/order must come from a
consistent source; this Map is memory-only, not across replicas,
and cannot recover WAL/offset position or guarantee external
exactly-once. Adapt to target DB transactions and CDC connector.
