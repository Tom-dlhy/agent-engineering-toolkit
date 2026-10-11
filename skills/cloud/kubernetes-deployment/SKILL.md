---
name: kubernetes-deployment
domain: cloud
version: "0.1.0"
description: >-
  Use when shipping container workloads to Kubernetes and configuring deployment, ingress, secrets, scaling or policies. Do not use for simpler hosting that meets the same requirements.
---

# kubernetes-deployment

## Workload
Define readiness/startup/liveness probes based on real behavior; configure resource requests/limits, safe rollout strategy, disruption budgets where needed and reasonable horizontal scaling.
## Security
Set restricted security contexts, namespace/service-account boundaries, NetworkPolicies, secret management and minimal RBAC. Avoid default privileged mounts and wildcard roles.
## Reliability
Understand failure recovery, scheduling, eviction and persistent volume lifecycle. Manage configuration/deployments via GitOps or reviewed declarative IaC. Make rollback and schema migrations explicit.
## Tests
Render and validate manifests, check policy compliance and dry-run against a suitable cluster. Test readiness, termination and rollback in staging before production release.
