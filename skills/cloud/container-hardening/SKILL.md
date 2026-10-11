---
name: container-hardening
domain: cloud
version: "0.1.0"
description: >-
  Use when packaging application runtimes into Docker/OCI images or hardening production containers. Do not use for non-containerized workloads.
---

# container-hardening

## Build
Use supported pinned base image, multi-stage builds and minimal runtime layers. Copy only required artifacts, run non-root where possible, set immutable labels and deterministic package locks. Never inject credentials into Docker build layers.
## Runtime
Use read-only filesystem where supported, drop capabilities, bound CPU/memory, limit exposed ports and provide explicit health checks. Ensure proper signal handling and graceful termination.
## Supply chain
Generate SBOM, scan base and application dependencies and verify signatures/provenance where infrastructure permits. Pin immutable image digests in sensitive deployments.
## Verify
Build and run a container smoke test, inspect image for secrets and vulnerable packages, validate expected configuration and document required runtime permissions.
