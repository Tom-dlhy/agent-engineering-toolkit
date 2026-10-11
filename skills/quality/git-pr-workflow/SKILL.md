---
name: git-pr-workflow
domain: quality
version: "0.2.0"
description: >-
  Use when creating, reviewing or updating Git branches and pull requests,
  resolving conflicts, applying review feedback or checking protected merge
  requirements. Do not force push shared refs or merge without authority,
  and do not assume PR mergeability implies release readiness.
---

# Git and PR workflow — controlled, reviewable changes

## Before writing
Inspect target repository, current branch/HEAD, required checks, branch
rules, issue/acceptance scope, dirty worktree and concurrent PRs.
Do not overwrite unrelated work or create duplicate branches.

## Execution
1. Branch from current base and preserve expected SHA. Use one coherent
   change per PR; split only when independent intent or rollback requires it.
2. Commit meaningfully, avoid secrets/binary surprises and avoid unrelated
   formatting noise. Run diff checks, appropriate tests and lockfile checks.
3. Open a Draft PR for unreviewed/refactoring work with scope, risks,
   evidence, untested cases and exact head/base revisions.
4. Address review threads with targeted patches; avoid silent ref changes
   or rewriting reviewers' approved code without justification.
5. Before any merge, re-evaluate check runs for **current head/merge queue**,
   approvals, ruleset/branch protection, conflicts and authorization.
6. No merge, publish or production action solely because CI is green
   or the API reports mergeable=true.

## Targeted references
- [Git branching, rebase and conflict safety](references/branching-and-conflict-safety.md) —
  **read when** choosing merge/rebase/cherry-pick, protecting history,
  resolving conflicts or working with concurrent edits.
- [PR review, required checks and rulesets](references/pr-review-and-merge-gates.md) —
  **read when** writing review findings, checking stale CI,
  merge queue and branch protection or handling security review.
- [GitHub Actions trust model](references/actions-pr-security.md) —
  **read when** the PR changes workflows, tokens, forks, checkout
  permissions or untrusted contributions.

## Boundaries
secure-code-review owns application vulnerabilities;
dependency-supply-chain owns package/action provenance; release-readiness
owns deployment GO/NO-GO. Report actual commit, tests, review state,
conflicts and merge status without claiming unauthorized actions succeeded.
