---
name: test-strategy
domain: quality
version: "0.1.0"
description: >-
  Use when choosing effective verification for a feature, refactor, bug fix or integration. Do not impose arbitrary 100 percent coverage or TDD ceremony on unrelated content-only edits.
---

# test-strategy

## Risk-driven coverage
Identify critical invariants, likely regressions and trust boundaries. Use unit tests for pure logic; integration tests for persistence, transport and cloud adapters; contract tests for provider interfaces; E2E tests for the most valuable user journeys.

Prioritize negative cases, error recovery, race/retry behavior and permission boundaries when appropriate. Keep tests deterministic, isolated and fast enough to run frequently; avoid excessive mocking of the system under test.

## Implementation
For a bug, first capture a failing regression test when feasible. For new features, choose TDD when behavior can be specified clearly; otherwise pair implementation and tests incrementally. Use fixtures/fakes deliberately and run relevant checks before claiming success.

## Evidence
State which risks the suite covers, what ran successfully and remaining gaps.
