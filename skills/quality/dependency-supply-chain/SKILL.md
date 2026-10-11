---
name: dependency-supply-chain
domain: quality
version: "0.2.0"
description: >-
  Use when assessing third-party package dependencies, lockfiles,
  CI actions, container images, build provenance, SBOMs, advisories or
  supply-chain compromise. Do not mistake CVE scans or stars for a
  comprehensive malware, license or runtime security audit.
---

# Dependency and build supply chain — identity before trust

## Audit and decisions
1. Identify the *actual resolved graph*: manifest + lockfile + optional/runtime
   groups + transitive packages, actions, images, build tools and remote scripts.
2. Record exact source and immutable artifact identifiers, trusted registry,
   required licenses/notices, maintainer history and install/build side effects.
3. Evaluate known vulnerabilities with ecosystem tooling and OSV/GHSA context;
   include reachability, exploit preconditions, patch/backport and exposure.
   Absence of an advisory does **not** imply absence of malicious code.
4. CI: minimal token permissions, no secrets to untrusted PR code, short-lived
   cloud identity/OIDC with constrained claims, pinned actions/digests and
   hardened self-hosted runner policy. Avoid unsafe pull_request_target checkout.
5. Artifacts: reproducible/pinned inputs where feasible; SBOM **identifies**
   components but is not a signature or proof of authenticity. Validate build
   provenance/attestations and registry/package identities where required.
6. Define update/canary/rollback, exception expiry and incident response.
   Audit any install script before execution; never copy/paste curl-pipe-shell.

## References
- [Dependency audit and remediation](references/dependency-risk-and-updates.md) —
  **read when** upgrading packages, analyzing advisories, transitive impact
  and balancing vulnerabilities against compatibility.
- [CI, workflow tokens and untrusted PRs](references/ci-identity-and-actions.md) —
  **read when** reviewing workflows, GitHub Action SHA pins, OIDC secrets,
  pull_request_target or external build execution.
- [SBOM, provenance and artifact release](references/sbom-provenance-and-response.md) —
  **read when** publishing packages/images, evaluating SLSA, verifying
  attestations, generating inventories or containing an incident.

## Distinct boundaries
external-skill-audit handles *agent skill* provenance/prompt injection
rather than general package dependencies. secure-code-review handles
application exploit paths. git-pr-workflow handles review and branch
rules; release-readiness performs final deployment decision.
No automatic dependency install, network scripts or credential changes
without authorization and environment checks.
