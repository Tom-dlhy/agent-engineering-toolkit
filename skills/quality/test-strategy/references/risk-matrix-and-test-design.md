# Risk-driven test design, fixtures and trustworthy evidence

**Read when:** translating requirements into test coverage, deciding unit versus
integration scope, writing pytest fixtures or assessing coverage quality.

## From risk to an executable oracle

For every changed use case, list (1) observable invariant (2) input/state
boundary (3) failure consequence (4) cheapest falsifying test. Prioritize
authorization, financial/persistent state, error translation and important
customer journeys. Never use line coverage as a correctness percentage:
100% executed statements can still miss missing branches, races and security
invariants. Branch coverage and mutation testing can expose gaps, but neither
proves production safety.

| Requirement | Test level | Oracle |
|---|---|---|
| Explicit PATCH null not silently erased | API contract | 422/contract-defined handling; DB unchanged |
| Reject another tenant's resource | Route+real DB integration | 403/404 and zero cross-tenant rows |
| Retried POST not double-charge | Fault-injected integration | One durable external effect |
| Publish schema change | Consumer contract | Old and new payloads interoperate |
| Core user checkout flow | Browser E2E | User-visible success and recoverable error |

## Deterministic fixture design

~~~python
import pytest

@pytest.fixture
def resource_store():
    store = {}
    yield store
    store.clear()

@pytest.mark.parametrize(
    "candidate,accepted",
    [("valid", True), ("", False), (" " * 5, False)],
)
def test_name_validation(candidate, accepted):
    result = bool(candidate.strip())
    assert result is accepted
~~~

This example tests a **local illustrative rule**, not a production validator.
Prefer fixture teardown that reliably closes files, HTTP clients, sessions and
transactions even on assertion failure. Session-scoped mutable fixtures leak
state across tests; use them only when reset/immutability is provable. Avoid
autouse network mocking that hides real integration regressions.

## Double selection

- Fake the upstream service when testing *your* translation/branch logic.
- Prefer a real database/transaction for isolation and unique constraints;
  SQLite in-memory is not a faithful stand-in for PostgreSQL isolation.
- Mock clock/UUID/side-effect API at the ownership boundary rather than mock
  every internal function.
- Test public behavior, not implementation method-call counts, unless an
  invariant specifically requires exactly one external effect.

## TDD and mutation evidence

A red-green-refactor loop helps where the required behavior is already clear;
exploratory research can start with a spike and add contracts once discovered.
A mutant surviving a test suite is a prompt to examine its semantics, not
automatic grounds for rejecting every PR. Keep coverage threshold as a
baseline guardrail, not a design metric.

## Acceptance record

Map each requirement to test path/command and proof environment. Distinguish
unit passing from full-stack passing. Note skipped/flaky tests and known
unsupported platform combinations. QA must never claim tests that have not
actually run.

Official sources: https://docs.pytest.org/en/stable/how-to/fixtures.html and
https://docs.pytest.org/en/stable/how-to/parametrize.html and
https://martinfowler.com/articles/practical-test-pyramid.html .
