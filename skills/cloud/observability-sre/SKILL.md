---
name: observability-sre
domain: cloud
version: "0.2.0"
description: >-
  Use when defining service-level SLIs/SLOs, runbooks, actionable alerts and cross-cloud traces/metrics. Do not use for log-format-only Python coding or generic local debugging.
---

# Cloud observability and SRE

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Start with user-visible success, latency, correctness and freshness SLIs. Separate request availability from CloudWatch/Azure Monitor/Cloud Monitoring collection success; define alert windows and burn-rate policies.
3. OpenTelemetry propagation is not authentication. High-cardinality tenant IDs/raw paths can blow up metric cost and leak data. Avoid full prompts, secrets and unapproved PII in traces/logs.
4. Inject 429/5xx/DB queue backlog and exporter outage in authorized staging; confirm traces correlate across services, alerts fire on sustained user harm and silence on transient nonactionable exceptions.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Cloud observability and SRE cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
