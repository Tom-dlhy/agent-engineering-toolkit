---
name: observability-sre
domain: cloud
version: "0.1.0"
description: >-
  Use when instrumenting application logs, traces, metrics, service reliability objectives and incident diagnostics. Do not use to install a full observability platform for an unobserved prototype without need.
---

# observability-sre

## Signals
Start from user-visible operations and failure modes. Define SLIs and realistic SLOs (availability, latency, correctness, freshness). Instrument traces across API, workers and cloud SDK boundaries; correlate logs via request IDs.
## Privacy and cost
Redact secrets and personal data; set sampling, retention and cardinality budgets. Avoid per-user IDs as unbounded metric labels. Distinguish health checks from actual customer success.
## Operations
Create actionable alerts on burn rate and sustained failure, not every exception. Build a short runbook with dashboards, expected baselines, rollback paths and on-call ownership.
## Verify
Simulate errors, timeouts and queue backlog in staging; confirm signal propagation and that alerts are useful without noise.
