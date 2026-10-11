# Progressive release, canary and operational stop criteria

**Read when:** deploying high-impact API/UI/cloud changes, choosing
canary/rolling/blue-green or monitoring a release for regressions.

## Select delivery mode for actual risk

| Method | Appropriate when | Tradeoff |
|---|---|---|
| Single controlled release | Small reversible/internal service | All traffic receives change at once |
| Rolling deploy | Compatible old/new versions, horizontal replicas | Two app versions coexist, schema compatibility needed |
| Canary | Key SLIs observable, traffic can be routed in increments | Requires enough volume for meaningful signal |
| Blue/green | Parallel identical environments and cutover | Cost and state/database complexity |
| Feature flag | Separating code shipping from exposure | Flag/variant lifecycle, stale feature behavior |

No strategy makes an irreversible data write automatically reversible.
For canary, monitor **user-impacting** SLIs: error rate, p95/p99,
successful task completion, DB load and downstream queues; compare
control population and traffic mix. A sample of 10 users is not proof
of no rare defects.

## Release runbook

Preflight artifact identity + backup restore status → authorized deploy
→ smoke via allowed endpoints → compare SLI/error-budget and traces →
go/hold/rollback decision → communication and flag cleanup. Define
operator, escalation, alert routing and response time in advance.
Record rollout timestamps/version so incidents correlate to the change.

## Stop conditions

A new cross-tenant data exposure, unexplained irreversible side effect,
SLO-breaching sustained 5xx or corrupted persistence stops rollout
even if CI remains green. Automatic rollback should be conditioned on
reliable signals; false positives can cause deploy oscillation.

## Aftercare

Verify background jobs, delayed consumers and cached clients, not just
immediate 200 health. Release can break an async pipeline minutes later.
Document known debt, remove temporary bypasses and schedule follow-up
without claiming it already happened.

Official: https://sre.google/sre-book/service-level-objectives/ and
https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions .
