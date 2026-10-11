# Git branching and safe conflict resolution

**Read when:** creating PR branches, rebasing, cherry-picking, resolving
conflicts or integrating simultaneous contributions.

## Start safely

Check git status, current branch, base SHA, open PRs and uncommitted work.
Prefer non-destructive branch from current main. An automated agent
should not overwrite user work, hard reset an unknown checkout or
force-push a shared branch. Use expected HEAD SHA when updating remote
refs to avoid racing another writer.

## Conflict handling
1. Identify actual conflicting hunks and both sides' intended behavior.
2. Inspect surrounding calling code, tests and business decisions.
3. Resolve semantically rather than blindly accepting ours/theirs.
4. Rerun tests touching merged paths and inspect diff/whitespace,
   no conflict markers left.
5. Avoid rebasing public/shared branches without collaboration plan.
6. If new base commits alter behavior, reassess risk and CI context.

Example: two branches touch a DTO field in different ways; a mechanical
merge may compile yet change serialization/validation semantics.
Review endpoint and consuming app contract, not just YAML mergeability.

## Reviewable commits

Small coherent commits with reproducible messages and no secrets.
Choose merge/rebase/squash according to repository policy; all can
preserve functional behavior when done correctly. Signing/provenance
adds integrity evidence but not correctness guarantee.

## Exit

Exact head/base SHA, merged/conflicting files, test results on resulting
tree and explicitly unperformed operations.

Official: https://git-scm.com/docs/git-merge and
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-pull-requests/about-pull-requests .
