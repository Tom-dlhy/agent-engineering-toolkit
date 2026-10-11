# OCI/Docker image and runtime hardening — security and operational verification

**Read when:** interpreting production failures, reviewing dangerous changes, measuring reliability or validating CI/gateway/infra rollout.

## Important failure boundaries
Check image for embedded tokens, vulnerable packages, unusual setuid/capabilities, unsafe writable paths, root privilege, runtime memory/CPU limits and multi-arch compatibility. Confirm reproducible image digest on CI target.

## Security and identity
Use least-privilege identities and workload federation, separate testing and production accounts/subscriptions/projects and authenticate before every privileged operation. Never treat a tool's successful invocation as a user-authorization check. Raw secrets, plan state and customer data may persist in logs, caches or telemetry.

## Release procedure
- Capture current version and approved deployment environment.
- Validate syntax/config and **negative tests** for missing permissions, malformed input, resource exhaustion and cancellation.
- Inspect actual cloud control-plane permissions and state diff in authorized staging; don't use destructive commands as discovery.
- Test rollback/recovery, user-visible SLOs and cloud billing/egress under representative workloads.
- Require manual approval and auditable change record for IAM, networking, DNS, data deletion and production deployment.

## Anti-pattern
Static best-practice checklists alone are not production proof. Document the precise observed evidence and what is unverified (cost estimates, live IAM grants, regional quotas, benchmark, disaster recovery) instead of marking all architecture production-ready.

## Official references
- https://docs.docker.com/build/building/secrets/
- https://docs.docker.com/build/building/multi-stage/
