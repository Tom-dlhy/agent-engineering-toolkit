---
name: finops-engineering
domain: cloud
version: "0.1.0"
description: >-
  Use when estimating and optimizing cloud spend, unit economics, utilization, egress and managed-service tradeoffs. Do not invent current prices without validating provider pricing.
---

# finops-engineering

## Baseline
Gather region, service usage profile, active users, data volume, storage retention, idle time, p95 peaks and growth assumptions. Obtain current pricing from provider calculators when needed.
## Analyze
Model compute, networking/egress, databases, API requests, build/CI minutes, monitoring and support. Separate fixed, variable and scale-triggered costs. Attribute to product feature or workload.
## Optimize
Right-size resources based on measurements; consider serverless idle economics, data locality, reservations and storage tiers. Assess engineering effort and reliability risk before reducing spend.
## Report
Provide a monthly cost range with assumptions, sensitivity cases and alerts/budget guardrails; never describe an estimated saving as a guaranteed outcome.
