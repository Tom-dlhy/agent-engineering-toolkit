---
name: aws-iam-security
domain: cloud
version: "2.0.0"
description: >-
  Use when designing or diagnosing AWS IAM roles, trust and resource policies, cross-account access, role federation, STS or least-privilege authorization. Do not use for app-level authorization only or unrelated Azure/GCP identity.
---

# aws-iam-security

## Scope

IAM identity policies, role trust, resource policies, SCPs, permission boundaries, session policies, STS and Access Analyzer. This is about **AWS authorization**; application authorization remains a separate layer.

## Decision procedure

1. Identify **principal → action → exact resource ARN → request context → expected outcome**.
2. Determine the caller identity and invocation context (Lambda execution role, ECS task role, CI OIDC role, local SSO). Do not guess which principal actually made the call.
3. Identify all policies involved: identity, trust (assume role), resource, KMS key, SCP, boundary and session; an explicit deny prevails over an allow.
4. Grant minimum service actions on minimum resources. Where an action cannot be resource-scoped, isolate it and document the necessity.
5. Validate and simulate policy semantics before rollout; avoid broad `*`, over-permissive `Principal` and permanent access keys.

## Load only relevant references

- [Policy construction and evaluation](references/policies-and-trust.md) — when writing policies, assume-role trust, cross-account S3/KMS or diagnosing AccessDenied.
- [Federation, identity and audit](references/identity-and-diagnostics.md) — when using CI OIDC, workload roles, STS, CloudTrail or permission troubleshooting.

## Done when

The actual calling principal is known; effective authorization path and least-privilege actions documented; explicit deny/permissions boundaries considered; only the intended account/resource receives access; failure and negative-access tests recorded.
