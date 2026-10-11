---
name: terraform-iac
domain: cloud
version: "0.2.0"
description: >-
  Use when designing IaC modules, remote state, provider lockfiles, plan diff, drift detection and controlled infrastructure rollout. Do not use for an unapproved apply/destroy or one service's application-level SDK code.
---

# Terraform/OpenTofu infrastructure as code

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Modules should express narrow capabilities, typed variables/outputs, pinned providers and isolated state by environment/security boundary; do not use workspaces as automatic tenant isolation.
3. Remote backend with access policy and locking where supported; backends have **optional locking**, don't claim every backend locks. Terraform plans and state can expose sensitive values including when CLI hides them; secure artifact retention.
4. GitHub PR runs fmt/validate/plan with read-only credentials; apply/destroy require explicit authorized workflow/environment approval, exact plan match, replacement/deletion review and rollback strategy. Check moved/import blocks for safe migrations.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns Terraform/OpenTofu infrastructure as code cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
