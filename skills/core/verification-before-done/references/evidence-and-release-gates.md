# Verification — proof ledger, completion and release handoff

**Read when:** presenting implementation completion or reviewing CI, PR, deployment
preparation and risk before reporting a result.

## Evidence ledger (example, not real checks)

| Claim | Command/scenario | Revision / environment | Result | Limitation |
|---|---|---|---|---|
| Reject invalid API payload | `pytest tests/test_api.py -q` | PR SHA / Python 3.x | PASS | HTTP adapter mocked |
| Migrate DB safely | Staging backfill + rollback | Staging DB | BLOCKED | No staging auth |
| UI menu keyboard | Browser/AT test | Browser target | SKIPPED | Browser unavailable |

Replace illustrative entries with **executed** results. A check is sufficient
only for outcomes actually asserted by it; CI being green is necessary for
workflow policy but never proof of unrelated external correctness.

## Completion states

- VERIFIED IN SCOPE: observed checks cover specified behavior on current revision.
- PARTIAL: some acceptance criteria proven, limitations named.
- BLOCKED: missing authorization, env/tool access or test fixture.
- NOT COMPLETE: known failing relevant test, contract break or unresolved blocker.

GitHub `mergeable` is a version control status and does not mean ready for production
or authorized to merge. A passing check may become stale after branch changes.

## User-facing report

"Changed X to enforce Y. Unit suite A passed on SHA Z. End-to-end provider tests
were not run because credentials are unavailable. No production deployment/merge."
Never copy fictional counts from sample reports. Exact revision, command, result
and remaining risk allow another reviewer to verify independently.

## Authorization gates

Tests, PR review, merge, migrations, publishing, destructive operations and privileged
cloud changes have separate permissions. Green tests cannot authorize a merge. If
user asked for review-only, do not mutate. If user asked for PR-only, leave in Draft.

## Failed verification

State original failure, whether it is fixed, and what remains unresolved. A retry
without causal understanding can hide flaky behavior. Route actual diagnosis to
systematic-debugging; route broad quality plans to test-strategy.

Background: https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/using-workflow-run-logs and https://docs.pytest.org/en/stable/ .
