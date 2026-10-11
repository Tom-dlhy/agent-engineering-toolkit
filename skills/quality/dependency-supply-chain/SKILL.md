---
name: dependency-supply-chain
domain: quality
version: "0.1.0"
description: >-
  Use when securing third-party packages, GitHub Actions, container images, SBOMs and external skill sources. Do not accept popularity or current star counts as proof of safety.
---

# dependency-supply-chain

## Intake
Pin dependency versions and generate lockfiles; verify maintainer provenance, release artifacts, license and transitive dependencies. Audit newly introduced install scripts and network side effects.
## CI guardrails
Use read-only default tokens, short-lived cloud credentials and immutable action references. Scan package and container vulnerabilities, secrets and IaC; tune for exploitable risk rather than failing on every low-priority warning.
## Third-party skills
Review SKILL.md instructions, referenced scripts/assets, GitHub revisions, external tool permissions and prompt injection risks. Track exact source SHA and required copyright notices.
## Incident readiness
Plan the ability to quarantine, roll back and rotate exposed credentials. Record what was verified and what remains unknown.
