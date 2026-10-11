---
name: ci-cd-engineering
domain: cloud
version: "0.1.0"
description: >-
  Use when designing GitHub Actions, deployment pipelines, quality gates or protected branch workflows. Do not add expensive jobs without a concrete coverage purpose.
---

# ci-cd-engineering

## Threat model
Treat PR source, third-party actions, artifacts, caches and workflow inputs as untrusted. Pin actions to vetted immutable SHAs, restrict GITHUB_TOKEN permissions, avoid untrusted code executing with privileged pull_request_target contexts.
## Pipeline
Split deterministic checks (format, manifest, unit tests, typecheck, build, security) by failure domain. Use cache keys tied to lockfiles, concurrency controls and bounded timeouts. Avoid pipelines where output is masked and failures appear green.
## Release
Separate validation from deployment. Use short-lived cloud credentials via OIDC and environment approvals before production. Ensure required status checks use stable, unambiguous job names.
## Review
Prove negative cases: intentional failing tests block merge, PR from untrusted branch cannot access secrets and protected branch cannot be pushed directly by ordinary contributors.
