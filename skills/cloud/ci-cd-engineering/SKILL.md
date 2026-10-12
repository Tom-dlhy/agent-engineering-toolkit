---
name: ci-cd-engineering
domain: cloud
version: "0.2.0"
description: >-
  Use when engineering GitHub Actions quality gates, OIDC deployment roles, protected environments and supply chain workflows. Do not use for a generic Git PR or frontend component unrelated to pipeline execution.
---

# CI/CD and federated cloud deployment

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Separate untrusted pull request verification from privileged deploy jobs. Pin actions immutable SHAs, constrain GITHUB_TOKEN, use environment approvals and repository/ref/environment claims for federated OIDC.
3. GitHub OIDC `id-token: write` permits requesting identity JWT but does NOT itself give cloud permissions; AWS/GCP/Azure trust policy grants cloud role conditioned on issuer/audience/subject. Tokens must never appear in logs.
4. Fork PR cannot read deploy credentials or request production role; a failing test must block promotion; concurrency prevents conflicting deploys; artifact provenance/SBOM and immutable build digest protect release chain.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns CI/CD and federated cloud deployment cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.

## Risk-scaled delivery pipeline methodology

Adapt GitHub's devops-rollout-plan preflight and immutable-artifact
principles. A pipeline is a separation of **untrusted verification**
from **authorized privileged delivery**, not merely a YAML file with green checks.

| Mode | Pipeline scope | Proof |
|---|---|---|
| LIGHT | Docs or small CI fix with no permissions change | Syntax/diff and safe non-privileged job |
| STANDARD | New test/build gate, artifact upload or dependency update | PR event simulation, build SHA, least-privileged token |
| DEEP | OIDC/IAM, deploy permissions, protected environments, release promotion | Fork/PR denial, pinning, artifact provenance, environment approval and rollback drill |

**Preflight:** inspect trigger types (PR from fork, push, tag,
workflow_dispatch), effective token permissions, reusable workflows,
environment protections and who can edit workflow files. Untrusted
PR payloads must not flow into privileged shell code. Avoid exposing
secrets to untrusted jobs, and never use a privileged pull_request_target
context to run fork code without isolation.

**Verification graph:** source SHA -> immutable built artifact digest ->
test result -> signed/provenance record where configured -> staging
artifact -> promoted production digest. A green test on SHA A does not
prove a different rebuilt artifact B is equivalent. Check dependency
pinning, timeout/cancel races and protection rules. Distinguish test
completion from release authority.

**Deployment path:** stage progressively only with authorization;
measure error rate, latency, queue depth and business invariants
against a baseline. Establish rollback triggers, owner and safe
data-migration limitations *before* enabling production writes.

Example: a workflow grants id-token: write. That allows requesting an
OIDC token, **not** a cloud role; AWS/GCP/Azure trust policy must still
bind issuer/audience/subject and environment. Negative-test a fork PR
and a tag from unauthorized ref in a disposable repo, not production.

Output exact workflow ref, job run IDs, trigger/permission matrix,
artifact checksum, failed/skipped gates and unapproved deploy actions.
