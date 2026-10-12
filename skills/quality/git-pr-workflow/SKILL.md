---
name: git-pr-workflow
domain: quality
version: "1.0.0"
description: >-
  Use when creating or finishing isolated Git branches/worktrees, opening or
  reviewing pull requests, assembling review evidence, resolving conflicts or
  deciding a safe integration path. Do not force push, erase another worktree,
  merge, publish or deploy without explicit authorization.
---

# Git and PR workflow — reversible, reviewable integration

## Ownership and initial inspection

Git branches and worktrees protect distinct work; they do **not** themselves
prove changes are safe. Inspect repo path, current/ref base SHA, branch
protection, dirty/untracked files, existing worktrees, live PR state and
pending reviews before writing. Preserve user-owned work. A green CI on
a stale SHA, API mergeable=true or a reviewer approval never independently
authorizes a merge. For a simple edit in an already isolated branch,
avoid making a second branch or a worktree just to look thorough.

## Decision by work complexity

| Evidence | Isolation and history | Review / integration |
|---|---|---|
| LIGHT, existing safe task branch | Work in place; narrow commits and targeted diff inspection | R0, no automatic PR/reviewer unless requested |
| STANDARD, multi-file or separate feature | New branch if required; worktree only if active work risks collision | PR with scoped description, CI, R0 or warranted R1 |
| DEEP, concurrent efforts, major migration/trust boundary | Isolated worktree or host-native equivalent, pinned base, explicit owner gates | R2 or required independent risk review, combined-tree checks, rollback/approval |

A worktree is a local isolation mechanism, not synonymous with parallel
execution. Detect whether the host already supplies isolated workspaces.
Never impose Git operations on a platform with a superior native mechanism.

## Execution protocol

1. Determine task authority, base and HEAD; inspect status, worktrees,
   locks, CI policy and files likely to overlap.
2. Select smallest safe isolation: current branch if safe; dedicated branch
   or verified worktree when other changes must be preserved. Refuse
   checkout/reset that would destroy uncommitted content.
3. Implement with coherent commits; inspect staged changes for secrets,
   generated artifacts, accidental scope and lockfile drift.
4. Verify exact changed revision with targeted tests plus impacted
   integration checks. Do not declare success from an older CI result.
5. Prepare a PR only when requested or when the agreed workflow requires
   one. Include intent, non-goals, base/head, test evidence, review R0/R1/R2,
   skipped checks, deployment/rollback considerations and open risks.
6. For feedback, inspect the *current* diff and use
   review-feedback-arbiter rather than blindly applying comments.
7. Before integration: recompute base, protection/ruleset, reviews,
   merge conflicts, approvals and actual combined-tree behavior.
8. Offer/execute the **authorized** integration choice; retain workspace
   and worktree for PR review if not merged. Cleanup only resources
   created for this task and verified safe to remove.

## Stop conditions and defensive defaults

STOP on unapproved merge, force push, release, production deploy or
destructive cleanup. STOP if the merge base is unclear, user edits would
be overwritten, conflicts have unknown semantics, expected SHA changed,
required CI is failing or a security blocker remains. A failed merge/CI
is evidence to investigate, not a cue for --force. Do not remove
another person's worktree or branch; no git clean -fdx as a routine step.

## Selective local references

- [Git branching, rebase and conflict safety](references/branching-and-conflict-safety.md)
  — **read when** choosing merge/rebase/cherry-pick or resolving conflicts.
- [PR review, required checks and rulesets](references/pr-review-and-merge-gates.md)
  — **read when** checking approvals, protected branches or merge queues.
- [GitHub Actions trust model](references/actions-pr-security.md)
  — **read when** changing workflow permissions or untrusted CI.
- [Worktree isolation, host detection and cleanup](references/worktree-isolation.md)
  — **read when** parallel tasks need isolated checkout or an existing worktree may exist.
- [Minimal review packet and revision-safe feedback](references/code-review-handoff.md)
  — **read when** requesting R1/R2 or replying to comments across revisions.
- [Branch completion and safe integration](references/branch-completion.md)
  — **read when** finishing feature work, presenting merge/PR/retain choices or cleaning a worktree.

## Boundary and exit

verification-before-done owns evidence adequacy; release-readiness owns
deployable artifact and rollback; secure-code-review owns application
vulnerabilities; execution-orchestrator chooses agent scheduling.
Exit with exact branch/base/head, changed file list, commands/results,
review level, blockers, merge permission and workspace disposition.
