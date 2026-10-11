# Property-based, concurrency and fault-injection tests

**Read when:** repeated retries, unpredictable input combinations, asynchronous
interleavings or persistent state make ordinary example tests inadequate.

## Property-based tests need independent invariants

A property test should assert an independently stated contract, not compare
a function's output with itself. For example, a simple application operation
normalizing identifiers has these invariants: uppercase canonicalization,
no duplicates, sorted results, and membership preserved.

~~~python
from hypothesis import given, strategies as st

def normalize_identifiers(values: list[str]) -> list[str]:
    return sorted({value.upper() for value in values})

@given(st.lists(st.text(alphabet="abc", min_size=0, max_size=5)))
def test_normalization_properties(values: list[str]) -> None:
    result = normalize_identifiers(values)
    assert result == sorted(result)
    assert len(result) == len(set(result))
    assert set(result) == {value.upper() for value in values}
~~~

This is a stand-alone illustrative property suite; in a real project
the system under test is imported from the actual application and
the oracle comes from business requirements. Hypothesis can shrink
failures; retain minimized cases as regression fixtures.

## Race and state-transition contracts

For a database-backed order processing operation, test:
- Two callers with same idempotency key; exactly one persisted effect.
- A retry with changed payload; explicit conflict, no mutation.
- Failure after external commit but before local ACK; recover/reconcile.
- Concurrent update against stale version; 409/412 or documented outcome.
- Crash after DB commit and before queue ACK; consumer replay safe.
- Cancellation while waiting on lock or HTTP pool; resources released.

In-memory mocks cannot prove cross-worker durability, Postgres isolation
or lost-update prevention. Use real disposable DB/broker integration tests
and controlled failpoints where appropriate. Don't claim exactly-once
external side effects from at-least-once broker delivery alone.

## Fault matrix

| Inject | Expected invariant |
|---|---|
| 429/Retry-After | Bounded attempts, no retry storm |
| Connect/read timeout | Correct classification, preserved deadline |
| Invalid provider schema | Safe protocol failure, no partial durable commit |
| Partial streamed response | Never treat incomplete output as validated final JSON |
| Worker death | Durable job state and replay/reconciliation |
| Pool saturation | Backpressure, no unbounded memory growth |

## Operational caution

Random stress runs may expose a race but **do not prove absence of races**.
Record tested schedules, seeds, environment and number of repetitions.
Use only controlled staging/synthetic fixtures, never chaotic writes or
DoS load on public/customer infrastructure without permission.

Official: https://hypothesis.readthedocs.io/en/latest/ ,
https://docs.python.org/3/library/asyncio-task.html and
https://docs.pytest.org/en/stable/how-to/flaky.html .
