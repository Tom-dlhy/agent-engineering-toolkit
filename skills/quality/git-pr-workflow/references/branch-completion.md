# Finishing a development branch with tested, authorized choices

**Read when:** implementation is complete, the user must choose PR/merge/retain, or worktree cleanup and integration are being considered.

## Gate 1 — prove the current artifact

Run the relevant full affected suite on the exact candidate SHA, inspect
the complete branch diff and required lint/build/integration conditions.
If a test fails, halt readiness; do not present failing work as merge-ready.
Identify and record flaky/environmental failures rather than assuming
they don't matter. Check BASE and HEAD independently; an old green PR
run does not certify the current branch.

## Gate 2 — identify repository context and constraints

Determine whether this is a local normal checkout, linked worktree,
detached host-managed checkout or API-only branch. Determine real target
branch, its current head and merge-base; inspect branch protection,
outstanding reviews, merge queue and conflicts. If the target branch
is ambiguous or has advanced with incompatible changes, stop integration
until reconciled. Do not assume the base is main for every repo.

## Gate 3 — offer choices without performing side effects

When the user hasn't already chosen, propose:
1. Keep the branch and open/update a PR for human review;
2. Keep the branch unchanged for later;
3. Merge into the approved target only with explicit authorization and
   all repository/policy gates satisfied.

For detached HEAD or API-only environments, offer only supported
actions (e.g. branch/PR rather than pretending local merge is available).
The options are a handoff, not implicit permission. If a user asked only
to prepare a PR, do not also merge/clean the worktree. If already
authorized, execute the selected action, not all actions.

## Gate 4 — integration check

Verify expected target ref has not moved; if it did, recompute safety.
Integrate without force-push; rerun relevant checks on the actual merged
tree, not just the source feature branch. A semantic conflict in shared
types can survive textual conflict resolution. For deployable code,
release-readiness independently gates production rollout. A merge
is not automatically a deploy.

## Gate 5 — cleanup ownership

Keep worktrees/branches in place if review remains pending. After an
authorized completed integration, clean only this task's known
worktree and local branch, verifying no uncommitted/untracked work.
Never erase another actor's branch, use force removal by default,
or delete user files as a convenience. The user can explicitly ask to
discard a branch, but destructive deletion must identify the exact
objects and consequences first.

## Exit artifact

State: branch/target SHA, current tests, R0/R1/R2 evidence,
unresolved findings, authorization state, PR link or merge SHA,
workspace retained/cleaned and unperformed follow-ups. Do not
describe a created draft PR as merged or a mergeable PR as reviewed.
