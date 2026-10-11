---
name: kubernetes-deployment
domain: cloud
version: "0.2.0"
description: >-
  Use when deploying Kubernetes Deployments/Services, probes, RBAC, NetworkPolicy, secrets and rollout strategies. Do not use for simpler managed Cloud Run/Container Apps solutions that meet requirements.
---

# Kubernetes workload deployment

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Differentiate startup probe (initialization), readiness (receive traffic) and liveness (restart deadlocked process). A failing readiness stops routing; a failing liveness triggers restart, not a trivial interchangeable health check.
3. Use service accounts with bounded RBAC, namespace policy, restricted PodSecurity, resource requests/limits, admission and NetworkPolicy provider support. Plan disruption/rollout/termination and storage migration separately.
4. Check rendered manifests and schema against exact cluster version, simulate failure/readiness, SIGTERM grace, secret/iam behavior, pods evicted and rollback under traffic. Never dry-run a live cluster without confirming context and permissions.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Kubernetes workload deployment cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
