# Debugging — evidence gathering and isolation

**Read when:** intermittent, environment-dependent or cross-boundary failures need
a controlled reproduction and a falsifiable hypothesis.

## Evidence states

Observed: exact errors, inputs, timestamps and versions. Correlated: recent diff,
metrics and coincident event. Hypothesis: mechanism with a disproof. Confirmed:
controlled test reproduces and removing the cause prevents it. Unknown: report missing
data instead of pretending a definitive diagnosis.

## Reproduction ladder

1. Preserve sanitized error, revision, runtime/SDK, seed and minimal input.
2. Execute smallest failing test or replay in isolated staging; do not copy secrets or PII.
3. Contrast local, CI and production: concurrency, timezone, feature flags, network,
   credential scope, caches, isolation level, worker count and package resolution.
4. Trace input → transformation → adapter → DB/network → response; identify first
   incorrect invariant, not merely final traceback.
5. If recent regression, use bisect only with reliable pass/fail oracle.
6. For flakes, bound repeated runs and vary concurrency/ordering deliberately.
7. For unavailable services, inject a deterministic timeout/429/invalid payload in a
   fake transport. Mocks establish local behavior, not provider availability.
8. If reproduction is impossible, document uncertainty and propose minimum bounded
   instrumentation with retention/authorization.

## Hypothesis ledger

| Hypothesis | Supporting observation | Disproof check |
|---|---|---|
| HTTP pool exhausted | Pool wait increases with concurrency | Measure pool wait at fixed load and controlled pool |
| API PATCH null violates invariant | Parsed DTO admits explicit null | Send both {} and {"name": null}; compare DB effect |
| Retry duplicates order | Same request occurs twice | Simulate commit-then-timeout; inspect durable idempotency |
| Cached config hides env change | Production process retains old value | Test isolated startup and cache reset |

Use one manipulated variable per controlled experiment when possible. Repeated timing
correlation alone is not a causal proof.

## Failure modes

Don't add logging of access tokens, prompt inputs, private records or customer emails;
avoid blind restart/unbounded retry, disabling test assertions and executing destructive
migration commands for diagnosis. For high-stakes incidents, escalate to explicit
operational authority before mutation.

References: https://docs.pytest.org/en/stable/how-to/flaky.html and
https://docs.python.org/3/library/pdb.html . Specific framework bugs require its
version-matched documentation, not generic advice.
