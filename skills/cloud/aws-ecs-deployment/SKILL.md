---
name: aws-ecs-deployment
domain: cloud
version: "2.0.0"
description: >-
  Use when deploying or operating applications in Amazon ECS or Fargate, task definitions, service rollout, container IAM roles, networking, ALB, autoscaling, secrets and graceful shutdown. Do not use for Lambda-only workloads or generic Docker build tweaks.
---

# aws-ecs-deployment

## Scope

ECS cluster, task definition, service, deployment strategy, image, CPU/memory, task networking, ALB target health checks, autoscaling, task role vs execution role and secrets. For Docker image security use `container-hardening`; for Terraform modules use `terraform-iac`.

## Decision procedure

1. Determine workload type: long-running API/worker, ephemeral job, scheduled task; choose ECS service or `RunTask`, and Fargate vs EC2 based on real constraints.
2. Inspect app port/health, container image provenance, region, account, CPU/memory, required egress, persistent state, secrets and SLOs.
3. Establish task role for the app and execution role for the ECS agent; scope each separately.
4. Design private subnets, security groups, load balancer or internal connectivity, log delivery, scaling, deployment rollback and cost.
5. Ensure PID 1 handles SIGTERM, drains requests and exits before stop timeout; verify target health checks use the correct path/port.

## Targeted references

- [Task identity, networking and service definition](references/task-and-network.md) — open for task role, secret injection, subnets, ALB, security group and task configuration.
- [Deployment, scaling and operations](references/release-and-operations.md) — open for CI/CD, health checks, autoscaling, circuit breaker, capacity and incident recovery.

## Exit criteria

Image pinned, secret and role boundaries tested, inbound/outbound networking least-privileged, healthy rollout and rollback demonstrable, failure and shutdown cases exercised, operator alarms and ownership documented.
