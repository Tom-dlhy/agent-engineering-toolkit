# Verification — choose and execute meaningful checks

**Read when:** selecting evidence after a code change or troubleshooting false green
test runs, skipped suites or environment mismatches.

## Match proof to claim

| Claim | Suitable evidence | What it cannot prove |
|---|---|---|
| Python DTO validation | Focused pytest schema/negative paths | Cloud credentials |
| HTTP partner mapping | MockTransport contract test | Upstream live quota/version |
| DB migration safe | Staging forward/rollback and locking check | Full production scale |
| Accessible dialog | Keyboard + assistive tech on target browser | Every WCAG criterion |
| Async worker durable | Kill/restart replay and idempotency test | Global exactly-once |
| LLM adapter functional | Mock SDK and authorized sandbox call | Model answer quality |
| Docs/links correct | Render and link/syntax validation | Runtime behavior |

Run from correct root/dependency lock/runtime. If a check is costly/destructive,
obtain authority before live access. Distinguish tests skipped by framework from
test command never executed.

## Shell and exit codes

~~~bash
set -o pipefail
python -m pytest tests/test_api.py -q | tee /tmp/test-output.log
~~~

This is Bash-specific illustrative syntax; PowerShell/Windows semantics differ.
Without pipefail the terminal exit status may be that of tee, not pytest.
Never hide a failing stage with arbitrary `|| true` or truncated log views.
If command errors, capture failure and rerun the relevant stage after a fix;
do not selectively showcase green retries.

## Scope by impact

- LIGHT: diff check and focused validation.
- STANDARD: targeted unit/contract and type/build checks.
- DEEP: risk-specific security, staged migration, rollback, negative concurrency
  checks and optional independent verification.

No mode provides license to mutate production secrets or third-party accounts.
A synthetic test suite with mocked upstream does not establish real provider
capability, latency, costs or tokenization.

## Handling blockers

Mark BLOCKED when credential, runtime, device or permission absent; SKIPPED when
unnecessary with a documented rationale; FAIL when a relevant check failed.
The requirement to be accurate supersedes the desire to say "done".

Background: https://docs.pytest.org/en/stable/ and
https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/using-workflow-run-logs .
