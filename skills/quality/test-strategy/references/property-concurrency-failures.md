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

## Risk-based RED/GREEN and test-oracle challenge

**Read when:** tests cover retries, parallelism, user authorization,
state machines or bugs that can pass a naive happy-path assertion.

### Build an oracle from invariants

For a cross-tenant route, assert denial **and** no leaked result,
metadata, audit privilege or unauthorized DB write. For retryable
remote effects, assert exactly-once *observable business result* with
a stable idempotency token even after local timeout. For migrations,
assert old and new consumer compatibility across staged release order.
Do not mirror implementation logic inside a mock as the test oracle.

A useful mutation test removes the guard or changes a branch condition.
If the test stays green, it fails to detect the defect. This is an
oracle challenge, not permission to ship mutated code. Perform only
in isolated local/disposable workspaces.

### Red -> green -> safe refactor

1. Prepare fixture and expected observation.
2. Run on current buggy baseline; inspect whether failure is precisely
   the intended assertion. If test passes, check it isn't redundant,
   vacuous or testing the wrong call path.
3. Apply minimal code correction; run identical test and compare.
4. Refactor without weakening tests; verify negative and happy path.
5. Run integration/contract checks affected by the change, on exact HEAD.

Do not demand test-first for a typo or mechanical generated snapshot
where a direct output check is more meaningful. R2 requires real
security/data recovery evidence proportional to risk, not arbitrary
100% coverage.

### Controlled fault injection

Use disposable DB/services and inject faults at side-effect boundaries:
before commit, after commit before ACK, retry during in-flight
operation, duplicate event delivery, stale permission, and cancellation.
Record deterministic seed/order, expected durable state and cleanup.
A stress run without controlled interleavings cannot prove race freedom.
If the real broker/provider cannot be used, name that limitation.

Concrete case: document upload into object storage followed by DB row.
Fail object upload after metadata insert; assert no accessible orphaned
row or documented reconciliation state. Fail DB write after object upload;
assert compensating cleanup or recoverable orphan queue. Do not hide
partial-failure behavior behind a mock that always succeeds.

Method inspiration:
https://github.com/obra/superpowers/tree/main/skills/test-driven-development
