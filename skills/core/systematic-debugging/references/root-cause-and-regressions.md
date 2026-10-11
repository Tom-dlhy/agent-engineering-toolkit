# Debugging — causal patch and regression

**Read when:** a likely root cause is identified and a repair needs correctness,
security, race-safety and rollback verification.

## Red → green → adjacent checks

1. Add the smallest failing test asserting **intended behavior**, not a fragile error string.
2. Apply the repair where invariant is owned (transport validation, business policy,
   adapter status mapping, transaction, client lifecycle).
3. Rerun red test, then adjacent boundary, negative and concurrent tests appropriate
   to the bug. Check no new swallowing of errors or unauthorized side effects.
4. Compare behavior on old vs new revision if possible, record exact command/exit code,
   and inspect diff for unrelated changes.
5. For a production incident, distinguish containment, true root-cause fix and
   separate longer-term hardening. Design reversible rollout/feature flags as justified.

### Example — PATCH unset versus null
Observed: explicit null accidentally clears a nonnullable field.
Root: service uses `model_dump(exclude_unset=True)` but treats passed null as
permitted; empty `{}` is a different input. Tests:
- PATCH empty keeps existing field.
- PATCH `{"name": null}` rejects or follows an *explicitly documented clearing contract*.
- PATCH valid name changes it; conflict/tenant cases still pass.
Do not "fix" by indiscriminately using exclude_none if null clears other fields.

### Example — asynchronous log context
Observed: correlation ID disappears in queued logs. Investigate where formatter runs:
a ContextVar read in another thread/task might lack original value. Capture allowed
context when emitting record, test concurrent requests with distinct IDs and
confirm no cross-request leakage.

## Evidence classification

Proven: reproducible before/fails-after relationship under controlled conditions,
passing regressions. Probable: multiple supporting observations but no decisive
experiment. Unknown: missing environment/test. Do not present "one rerun green"
as validation of a flake.

## Exit questions

What triggered failure, which invariant was broken, who owned it, what experiment
disproved alternatives, what remains vulnerable, and what tests actually ran?

Sources: https://docs.pytest.org/en/stable/ and
https://martinfowler.com/articles/practical-test-pyramid.html .
