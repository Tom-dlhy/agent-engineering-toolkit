---
name: secure-code-review
domain: quality
version: "0.1.0"
description: >-
  Use when reviewing code touching auth, permissions, secrets, serialization, untrusted input, dependencies or cloud infrastructure. Do not use to manufacture speculative findings for harmless changes.
---

# secure-code-review

## Threat-first review
Identify assets, entry points, trust boundaries and attacker-controlled inputs. Inspect actual changed code plus surrounding calling context. Evaluate authentication vs authorization, least privilege, injection, data leakage, secret handling, logging, SSRF, CSRF, supply chain and unsafe deserialization where applicable.

## Report standards
For every finding give file/path, triggering conditions, plausible exploit or failure, severity, and actionable fix. Prioritize confirmed high-impact issues; label hypotheses. Suggest tests or static analysis that could falsify uncertain claims. No findings is acceptable.

## Boundaries
Do not fetch credentials, scan live third-party systems, attempt exploitation or execute scripts without explicit permission. Security review complements tests and dependency scanners; it does not replace them.
