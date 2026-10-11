---
name: cloud-provider-selection
domain: cloud
version: "0.2.0"
description: >-
  Use when comparing AWS, GCP, Azure, Cloudflare or portable architecture for a concrete workload. Do not use for a provider already fixed and only one SDK call is needed.
---

# Cloud provider selection and workload placement

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Compare explicit deployment options (managed serverless vs container vs DB/queue), compliance/region, team knowledge, latency, SLA, integration, cost, egress and lock-in; never compare brand adjectives.
3. Use current official capabilities/prices by region and account terms; map IAM, networking, quotas and data migration costs. Include non-production/staging, incident ownership, platform maintenance and exit path.
4. Write measured assumptions, confidence and benchmark plan. A cloud service's marketing autoscaling claim doesn't establish throughput for application DB and provider quotas. Prefer ADR with reversibility and sunset criteria.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Cloud provider selection and workload placement cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
