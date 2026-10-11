# ECS releases, autoscaling and production operations

**Read when:** planning deployment, health checks, graceful shutdown, autoscaling, rollback or debugging unhealthy tasks.

## Safe deployment workflow

1. Build tested multi-stage image from reviewed lockfile; scan packages; sign/provenance if supply chain requires it.
2. Push immutable image/digest; don't mutate a `latest` tag as the sole traceability key.
3. Register task definition revision and diff resource/role changes.
4. Update staging service; wait for **application** health (not just container running). Exercise critical API path and background worker behavior.
5. Inspect target health reasons, stopped task reasons, CloudWatch logs, CPU/memory and downstream error rate.
6. Promote via approved deployment gate; enable ECS deployment circuit breaker/rollback where appropriate; know rollback task revision and database compatibility.
7. Verify SLOs after deployment and record version/revision/image digest.

## Readiness and termination

- `/health` liveness should prove the process responds; deeper readiness may check essential dependencies within bounded time.
- With ALB, align health path, success codes, port, startup grace and deregistration delay with application behavior.
- On SIGTERM, stop accepting new requests, drain in-flight work and exit within configured stop timeout.
- For queue workers, release/complete work with idempotency and retry protection before termination.

## Scaling and cost

Capacity provider and service autoscaling metrics should reflect bottlenecks: CPU, memory, ALB request count, queue age/backlog per worker, or custom SLIs. Maximum instances must respect database connection budgets, downstream quotas and VPC IP space. Too many tasks can make tail latency and cost **worse** when a dependency is saturated.

## Incident runbook

| Symptom | Check first |
|---|---|
| Tasks keep restarting | Stopped reason, memory OOM, entrypoint, health check settings |
| Target unhealthy | Listener, port, route, SG, app startup, path and timeout |
| Cannot pull image | Execution role, ECR reachability, image digest/region, VPC endpoints/NAT |
| SDK AccessDenied | Task role vs execution role, resource/KMS policy, tenant scope |
| High latency after scaling | Database pool, connection count, queue backlog, downstream throttling |
| Deploy never stabilizes | Capacity, resources, health grace, circuit breaker, rollback safety |

Never execute ECS service update or change production networking without explicit approval.

Official: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html and https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html .
