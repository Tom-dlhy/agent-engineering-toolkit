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
