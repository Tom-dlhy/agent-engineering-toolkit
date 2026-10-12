# Worktree isolation, host-native detection and safe cleanup

**Read when:** concurrently implementing changes, using a linked Git worktree, preparing a feature branch with user changes already present, or assessing worktree cleanup.

## Step 0 — observe the checkout

~~~bash
git status --short --branch
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git worktree list --porcelain
~~~

git-dir differing from git-common-dir can indicate a linked worktree,
but nested submodules also have distinct Git metadata. Check the
superproject path before concluding a worktree exists. A detached HEAD
may be intentionally managed by the host; don't create/move a branch
without permission. Prefer the host's native worktree/isolation API
when verified available. A remote-only GitHub tool may support branches
but **not** create an accessible local worktree; don't pretend it did.

## Create an isolated workspace only when justified

1. Identify the exact base commit/ref, current user modifications and
   overlapping files. If already isolated, use it.
2. Prefer a project convention (.worktrees/ or worktrees/) or host-defined
   location. Before creating in-repo worktrees, verify ignore policy:
   git check-ignore -q .worktrees or equivalent. If neither ignored,
   request a safe configuration change rather than creating untracked
   recursive repository content.
3. Use a unique descriptive branch name and verify it doesn't exist.
   Typical command for a new local branch:
   git worktree add .worktrees/feature-auth -b feat/feature-auth origin/main
4. Run project setup according to verified lockfiles and instructions;
   don't install arbitrary packages/scripts during security inspection.
5. Establish the current test baseline in the newly isolated directory.
   Record existing failures so they are not falsely attributed to your diff.

Worktrees share Git object/ref storage. Two agents modifying the same
branch/ref, shared checkout path, generated assets or test database
can still race. Give each worker a file allowlist and independent
branch/worktree, and serialize integration of shared types/migrations.

## Cleanup is a separate, permissioned decision

Wait for the PR to be merged or explicitly abandoned. Check:
- location is the workspace **created for this task**, not an unknown path;
- working tree is clean and commits are backed by an intended ref/PR;
- no untracked user files need preserving;
- no other running agent uses the path;
- base/feature refs are verified and any merge integration tests passed.

Then use git worktree remove <verified-path> without --force. If Git
refuses because of dirty work, preserve the directory and report.
Delete a merged local branch with git branch -d only after user
authorization/accepted policy; never force-delete merely to tidy.
Don't remove all .worktrees/ or run git clean -fdx. Such commands can
destroy resumable progress ledgers or another actor's assets.

## Failure cases

If the current repo has uncommitted work, don't use git reset --hard
or git stash pop blindly. If a branch is already checked out in another
worktree, report its location and use that worktree or another branch.
If host-native isolation prevents writes, report the environment limitation,
execute only safe inspection, and seek permission before changing directories.
Always distinguish creating a Git branch via API from a real local worktree.
