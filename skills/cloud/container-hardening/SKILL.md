---
name: container-hardening
domain: cloud
version: "0.2.0"
description: >-
  Use when building hardened OCI images, enforcing least-privilege containers, reproducible builds and supply chain attestations. Do not use for serverless code without containers or arbitrary kubernetes role setup.
---

# OCI/Docker image and runtime hardening

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Use supported base image pinned digest, multi-stage build, deterministic lock, non-root user, no secrets baked into layers, explicit health/stop signals and needed capabilities only.
3. Docker build secrets via BuildKit secret mounts, not ARG/ENV; bind ports and read-only filesystem where workload permits. SBOM/provenance/scans are evidence but not a guarantee of zero vulnerabilities.
4. Check image for embedded tokens, vulnerable packages, unusual setuid/capabilities, unsafe writable paths, root privilege, runtime memory/CPU limits and multi-arch compatibility. Confirm reproducible image digest on CI target.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns OCI/Docker image and runtime hardening cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
