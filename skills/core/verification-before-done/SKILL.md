---
name: verification-before-done
domain: core
version: "0.1.0"
description: >-
  Use when reporting completion of coding, deployment preparation, documentation, data or infrastructure changes. Do not use as a substitute for running actual verification tools.
---

# verification-before-done

## Evidence gate
Before announcing success, inspect the diff and select checks that can prove the intended behavior: unit tests, integration tests, typecheck, linter, build, security scan, smoke check, migration dry-run or visual QA when appropriate.

Run commands in the project's documented environment. Preserve meaningful exit codes; be careful when piping commands through tail, grep or tee (enable pipefail where supported). Do not hide failures by rerunning selectively without reporting them.

## Reporting
Record each command with pass/fail/skipped, summarize real results and identify checks you could not run. Separate static inspection from execution. An agent review is not a replacement for an actual test.

## Failure
Investigate the failure or describe the blocker. Never mark a task verified because code merely looks correct.
