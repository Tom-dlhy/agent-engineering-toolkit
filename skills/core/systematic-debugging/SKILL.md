---
name: systematic-debugging
domain: core
version: "0.1.0"
description: >-
  Use when a bug, failing test, broken build or unexpected runtime behavior needs diagnosis. Do not use as an excuse to impose full incident-process overhead on known one-line mistakes.
---

# systematic-debugging

## Diagnose before patching
1. Capture the observed symptom and exact error, including environment, version and reproducible steps.
2. Identify the smallest reproduction. Read the relevant logs and recent diff.
3. Trace the data through component boundaries, starting near the first incorrect output.
4. Form one falsifiable hypothesis. Design the cheapest check that could disprove it.
5. Change one thing at a time; avoid speculative shotgun fixes.
6. Add a focused regression test when feasible, implement the fix, and verify it passes.

If you cannot reproduce, state what is missing and propose targeted instrumentation. Do not fabricate a root cause.

## Exit
Describe the root cause, the specific fix, regression protection, evidence and residual uncertainty.
