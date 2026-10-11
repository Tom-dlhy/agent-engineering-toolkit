---
name: finops-engineering
domain: cloud
version: "0.2.0"
description: >-
  Use when analyzing cloud cost allocation, budgets, deployment pricing, unit economics and billing guardrails. Do not use for choosing cloud solely from guessed retail unit price or model response text.
---

# FinOps spend and unit economics

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Measure compute idle/burst, storage and snapshots, networking/NAT/egress, managed DB, monitoring, queues, API calls and provider model tokens. Use cost per successful request/job as denominator instead of just total monthly spend.
3. Budgets/alerts are not always hard spend cutoffs; compare actual provider billing exports and list prices with commitments, regional fees, free tiers and data egress. Separate estimate vs observed spend vs forecast.
4. Tag/label ownership, account/project/subscription mapping, daily budget anomaly, cost by product feature/tenant and unit economy sensitivity; don't report precision or guaranteed savings without real billing evidence.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns FinOps spend and unit economics cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
