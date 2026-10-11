# Pull request evidence, code review and merge gates

**Read when:** opening/updating PRs, responding to review, checking
branch rules and deciding if a current revision is mergeable.

## Review surface

State intended behavior, scope, why alternative rejected, tests and
security/migration implications, screenshots or logs where meaningful,
remaining unknowns and exact revision. A generic "tests passed"
without SHA or target environment is weak evidence.

Review the diff **and necessary surrounding code** for contract changes,
state, data boundaries, auth and error handling; avoid style-only
noise. Group findings by severity and include file/line, preconditions
and impact. "No findings" can be a valid result.

## Actual branch/ruleset checks

- Required status checks for current head or merge queue commit,
  and whether checks are fresh after push.
- Required reviews, CODEOWNERS, discussion resolution and protection.
- Whether base moved, branch is behind and tests need rerunning.
- Security code scan and dependency review gates if configured.
- Whether Draft status signals incomplete review, not a merge blocker
  to be bypassed silently.

GitHub rulesets can require PRs, status checks and disallow force push;
availability depends on plan, repository visibility and admin settings.
API mergeable=true is Git's mechanical state, not permission to merge.

## Reviewer protocol

Separate factual defect, plausible risk and aesthetic preference.
Fix with minimal coherent commit, rerun relevant checks, update PR
description when review changes assumptions. Don't dismiss reproducible
review findings because formatter/linter passed.

## Final handoff

URL, current SHA, checks and review state, mergeable/blocked,
outstanding risks and whether the user authorized merge. Respect
instruction "PR only" even after green CI.

Official: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets and
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-pull-requests/about-pull-requests .
