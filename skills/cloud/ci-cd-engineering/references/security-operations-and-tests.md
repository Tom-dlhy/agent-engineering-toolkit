# CI/CD and federated cloud deployment — security and operational verification

**Read when:** interpreting production failures, reviewing dangerous changes, measuring reliability or validating CI/gateway/infra rollout.

## Important failure boundaries
Fork PR cannot read deploy credentials or request production role; a failing test must block promotion; concurrency prevents conflicting deploys; artifact provenance/SBOM and immutable build digest protect release chain.

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
- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication

## Secure release workflow negative-testing guide

**Read when:** GitHub Actions permission, OIDC federation, fork PR,
artifact promotion or production-environment trust is changing.

### Trigger -> privilege matrix

Enumerate pull_request, pull_request_target, push, tag and manual
dispatch, including fork/untrusted event constraints. For each
record checkout ref, effective GITHUB_TOKEN scopes, available
secrets, artifact access, environment guard and deployment role.
An untrusted PR must never execute arbitrary fork code under a
privileged write token or cloud role.

**Negative tests** in disposable repo/fixtures:
1. Fork PR cannot read deploy secrets or production cloud creds.
2. Tag on unapproved ref cannot promote artifact.
3. Changed source HEAD invalidates stale build/review evidence.
4. Cancelled prior deploy does not leave state silently promoted.
5. OIDC trust rejects invalid issuer/audience/sub/environment.
6. Artifact checksum promoted to staging equals the production
   candidate, not merely the same version string.

OIDC id-token: write is permission to request a JWT, not proof
a cloud resource trusts it. Validate cloud-side trust policy
with least privilege. Never log JWTs, service secrets or raw
private customer payloads to demonstrate denial.

### Deployment evidence chain

Use source commit -> built digest -> tests/scan -> approvals ->
signed/provenance evidence where available -> staging smoke ->
production digest -> post-deploy measured checks. Capture each
real run ID; unrelated green CI is not proof of a changed policy.

When a workflow touches deployment, preserve a rollback plan,
reconcile partial effects and separate CI pipeline changes from
live cloud role mutation. The latter needs explicit authorization.
Use safety checklists that actually exercise negative paths rather
than claiming security from YAML lint only.

Inspiration:
https://github.com/github/awesome-copilot/tree/main/skills/devops-rollout-plan
