---
name: git-pr-workflow
domain: quality
version: "0.1.0"
description: >-
  Use when organizing feature branches, GitHub Pull Requests, release merges, reviews and required CI gates. Do not bypass configured branch protection or merge without authorization.
---

# git-pr-workflow

## Branch strategy
Start from up-to-date main, work in feat/fix/docs branch, make cohesive commits and open focused PRs. Never force-push shared branches without explicit agreement.
## Quality gate
Check files changed, tests, relevant security implications and CI context. Prefer squash when project policy requires linear history; keep commit messages descriptive.
## Review
Attach concrete evidence, annotate meaningful risks and resolve review threads. Review changed code in calling context and focus on reproducible findings, not style trivia.
## Completion
Check target base branch, green required checks, protection status and mergeability immediately before merge. Human or user approval is required for merge if the workflow makes it a consequential action.
