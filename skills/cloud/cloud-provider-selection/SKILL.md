---
name: cloud-provider-selection
domain: cloud
version: "0.1.0"
description: >-
  Use when selecting between AWS, GCP, Azure, Cloudflare or portable infrastructure patterns. Do not use if the provider is fixed and only a local code change is needed.
---

# cloud-provider-selection

## Compare workloads, not marketing matrices
Gather geography, compliance, team expertise, expected traffic, data sensitivity, latency, cost ceiling, managed-service needs, observability, exit strategy and existing contract constraints.

Build a shortlist of concrete architectures and estimate monthly recurring costs with assumptions. Include data egress, observability, backups, networking and support. Compare reliability, access control, regional availability, maturity, pricing and operational burden.

## Lock-in analysis
Categorize dependencies: infrastructure IaC, service API, data formats, event semantics, IAM identity and deployment pipeline. Prefer stable protocols when cost-effective, but do not demand the lowest common denominator. Document any intentional vendor-specific optimization.

## Done when
Provide a scored or reasoned tradeoff, recommended stack, migration/exit cost and a short ADR. Verify current service capabilities and pricing against official provider documentation before making hard claims.
