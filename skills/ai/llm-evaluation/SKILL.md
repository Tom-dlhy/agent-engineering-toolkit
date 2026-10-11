---
name: llm-evaluation
domain: ai
version: "0.2.0"
description: >-
  Use when comparing model, prompt, agent or tool workflow quality,
  safety, accuracy, latency, spend and rollout readiness with evaluation
  datasets and representative failures. Do not assert superiority from
  a handful of subjective responses.
---

# LLM evaluations — reproducible decisions and bounded claims

## Procedure
1. Specify task population, business success criteria, risk severity,
   input distributions, human expectations and baseline version.
2. Build **held-out**, consented/redacted evaluation cases with
   labels/references, negative examples, multilingual and long-tail slices.
   Track data lineage and train/prompt contamination risks.
3. Separate deterministic checks (schema, tools, code execution, access
   denials) from answer grading and LLM-as-judge (subjective, biased).
   Calibrate judges with expert labels and blind comparative reviews.
4. Measure task success, abstention correctness, hallucination,
   unauthorized actions, cost per useful task, output/token
   completeness, latency distribution and retry burden.
5. Run repeated samples to assess variance; compare paired cases
   and report denominators, confidence/uncertainty and regressions
   by severity/slice rather than a single weighted leaderboard.
6. Gate release on predefined fail thresholds and an approved rollback.
   Treat high-risk failures as **blocking** even if aggregate score rises.
7. Monitor production drift and create authorized new evaluation cases
   from incidents; do not quietly train/optimize on the held-out set.

## Select references when appropriate
- [Datasets, labels, holdouts and leakage controls](references/datasets-and-leakage.md)
  — **read when** constructing gold sets or model/prompt comparison experiments.
- [Judges, metrics, statistical uncertainty](references/metrics-judges-and-statistics.md)
  — **read when** grading subjective outputs or claiming measurable improvement.
- [Release gates, online monitoring and incident-driven evals](references/gates-and-monitoring.md)
  — **read when** releasing, switching models or detecting distribution shifts.

## Ownership
rag-evaluation evaluates retrieval and grounding specifically;
agent-tool-safety owns security enforcement, not grading;
python-observability records runtime telemetry; llm-integration
implements model calls and validates output.

## Completion
Versioned evaluation corpus, reproducible run settings, clearly
scoped evidence, non-regression guardrails and honest unknowns.
