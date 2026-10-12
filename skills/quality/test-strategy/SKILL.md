---
name: test-strategy
domain: quality
version: "0.2.0"
description: >-
  Use when choosing and implementing risk-based unit, integration, contract,
  end-to-end, property-based or concurrency tests for software changes.
  Do not impose arbitrary 100% coverage or duplicate the evidence gate.
---

# Test strategy — prove contracts and failure behavior

## Intake
Read the requirement, current tests, runtime/toolchain and change surface first.
Identify business invariants, state transitions, trust boundaries, persistent
effects, external dependencies and likely regressions. Distinguish what can be
proven with fakes from what requires a real database/browser/provider.

## Decisions
1. **Pure rules** → isolated fast unit tests with representative boundary inputs.
2. **Database, HTTP, queues, third-party adapters** → integration/contract tests
   with realistic dependencies; test error, timeout, duplicate and cancellation.
3. **Public protocol or versioned schema** → producer/consumer contract checks
   including backward/forward compatibility; a generated OpenAPI schema is not
   proof a live endpoint conforms.
4. **Critical user journey** → a small number of browser/API E2E scenarios
   covering both success and recovery; prefer user-visible locators.
5. **Many combinatorial inputs/invariants** → property-based or metamorphic tests
   where a meaningful oracle exists, plus persisted regression examples.
6. **Parallelism, retries, races** → explicit deterministic interleavings or
   fault injection; don't claim one stress run proves race-freedom.

Choose a balanced portfolio by *failure cost and likelihood*, not percentages
or test-pyramid dogma. Preserve developer feedback speed by separating fast
PR checks, slower integration and authorized scheduled/load tests.

## Reference router
- [Test-design matrix and determinism](references/risk-matrix-and-test-design.md) —
  **read when** designing coverage from requirements, choosing fixtures/fakes,
  isolating test state or avoiding misleading coverage targets.
- [Integration, contract and E2E](references/integration-contract-e2e.md) —
  **read when** testing persistence, network APIs, event contracts, browser
  behavior or lifecycle against production-like components.
- [Property, concurrency and fault injection](references/property-concurrency-failures.md) —
  **read when** validating invariants over many inputs, idempotency, retries,
  crashes and hard-to-reproduce interleavings.

## Boundaries and exit
verification-before-done decides whether checks **ran** and support completion.
systematic-debugging investigates a failure. secure-code-review owns threat
hypotheses; this skill designs executable coverage for them. Report a
test-to-risk map, commands actually executed, isolation, pass/fail/skips
and remaining unverified conditions. Never invent test counts.

## Operational TDD and quality gates by cost and risk

Inspired by Superpowers' RED-GREEN-REFACTOR method. Test *invariants* rather than number of assertions or percentage coverage; a change that removes the guard should make the corresponding regression fail.

| Mode | Coverage | Avoid |
|---|---|---|
| LIGHT | One scoped oracle or static check and full intended diff | Expensive E2E for a typo |
| STANDARD | Focused unit, changed interface/consumer contract and negative case | Repeatedly testing unrelated systems |
| DEEP | Risk-led property, concurrency, replay, real disposable integration and rollback tests | Mock-only claims about production effects |

**RED validity:** the test must fail on old behavior for the intended assertion. An import error, unavailable cloud credential or flaky fixture is not evidence of the defect. **GREEN:** same test succeeds after minimal correction. **REFACTOR:** reorganize while re-running the oracle. For docs/generated artifacts select relevant checks; don't fabricate RED.

Choose oracle by boundary: pure domain rule -> unit; request/response shape -> contract; persistence isolation -> disposable database; browser hydration/accessibility -> real browser; retries -> controllable fault injector; permissions -> explicit denial and no data leakage.

**Mutation challenge:** invert/remove the changed guard locally and confirm the test fails. If it remains green, it does not test the desired behavior. Preserve a minimal regression fixture and avoid tests that only reimplement the production algorithm.

Worked case: tenant B accesses tenant A's document. Negative test demands denial and no content/metadata exposure. Run it before adding the ownership filter; then verify own-tenant read and real DB behavior if risk requires R2. A fake returning 403 independently of the SQL query does not prove tenant isolation.

Report requirement -> invariant -> oracle -> command -> actual result -> residual environment limit, distinguishing NOT RUN from PASS.
