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

## Causal debugging playbook and stop conditions

**Read when:** a bug has survived one attempted fix, a failure crosses
components or the diagnosis is uncertain.

### Minimal experiment matrix

| Observation | Proposed hypothesis | Disproving probe | Escalate if |
|---|---|---|---|
| Fails only on CI | race/shared fixture/runner difference | Reproduce at pinned seed/concurrency and compare local env | Same failure cannot be triggered under controlled conditions |
| Fails after deploy | config/contract/revision drift | Compare exact artifact digest and config, not only branch name | Customer data or permission boundaries involved |
| Duplicate remote action | timeout after remote commit | Fake provider commits then drops response | Real side effect may have been repeated |
| Test passes intermittently | order/time dependency | Repeat with randomized order and fixed fake clock | Flakiness hides security invariant |

### Verification steps

A fix request can include three states: observed symptom, causal claim,
and desired outcome. Link them with the smallest experiment: capture
trace or minimal fixture, predict observation before running, run it,
record result and eliminate/disprove alternative explanation. If the
observation is contrary to hypothesis, do not keep patching that
hypothesis. Prefer bisection when a reproducible historical boundary
exists; compare before/after environment only where inputs stay equal.

For behavior bugs prefer an observable RED failure and GREEN result;
record test name and exact SHA on both versions. The failure must be
the correct assertion, not import errors. For nondeterministic bugs
use controlled scheduling, event synchronization, fixed seeds and
state inspection rather than arbitrary timeouts. A synthetic
reproducer can establish a mechanism but not prove the real external
provider matches the same semantics.

### Defect-limiting safety

Never probe live customer records destructively, forcibly retry
payment writes, alter runtime auth or rotate secrets to "test" a theory
without explicit owner approval. If production symptoms continue but
reproduction is blocked, instrument safely with redacted correlation
IDs, measure incidence and report uncertainty.

### Exit record

Issue + source revision + first violated boundary + hypotheses
disproved + accepted cause confidence + test command/real result +
negative tests + external checks NOT RUN + user-visible remaining risk.
A patch with no causal evidence can be proposed as a guarded mitigation,
but must not be labeled a confirmed root-cause correction.

Primary inspiration:
https://github.com/obra/superpowers/tree/main/skills/systematic-debugging
