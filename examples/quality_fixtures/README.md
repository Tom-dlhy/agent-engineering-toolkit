# Quality fixture — illustrative, NOT a production ledger

A tiny deterministic, in-memory demonstration of tenant scoping,
replay/idempotency keys and input rejection. It has no real payments,
credentials or network requests. Run from repository root:

~~~bash
python -m unittest discover -s tests -p 'test_quality_contract_examples.py' -v
~~~

This is *not* safe for production persistence, parallel workers or
crash/replay correctness. Real operations require durable transactional
uniqueness, authenticated tenant identity and concurrent fault tests.
See the test-strategy and python-persistence skills for proper boundaries.
