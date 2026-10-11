---
name: llm-evaluation
domain: ai
version: "0.1.0"
description: >-
  Use when measuring prompt, model or agent changes for reliability, cost, latency and task success before deployment. Do not claim statistical improvement from tiny hand-picked samples.
---

# llm-evaluation

## Evaluation design
Define real task families, acceptance criteria, labels, failure severity and baseline. Use frozen representative datasets with leakage controls. Separate deterministic assertions from model-based quality judges.
## Metrics
Track exact pass/fail, hallucinations, structured-output validity, retries, human corrections, token input/output when available and p50/p95 latency. Slice by task type and failure mode.
## Method
Compare under controlled model/settings, multiple runs for nondeterminism and sufficient sample sizes. Preserve prompts/version identifiers and evaluation trace hashes without secrets.
## Decisions
Adopt only when measured benefit outweighs complexity and spend. Note uncertainty, limitations, regressions and rollback criteria.
