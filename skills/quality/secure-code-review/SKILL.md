---
name: secure-code-review
domain: quality
version: "0.2.0"
description: >-
  Use when reviewing software for exploitable trust-boundary defects,
  authentication/authorization flaws, injection, SSRF, secrets exposure,
  tenant isolation or unsafe operations. Do not invent vulnerabilities from
  aesthetic preferences or perform unauthorized active exploitation.
---

# Secure code review — trace untrusted data to sensitive effects

## Threat-first procedure
1. Establish feature purpose, threat model, assets, exposed entrypoints,
   authenticated roles, data sensitivity and affected deployment.
2. Compare modified code with caller/callee context. Map **source → validation →
   authorization → sink** and account for config, workers and persistence.
3. Prioritize object/tenant authorization, session/cookie/CSRF policy,
   server-side request destinations, SQL/shell/template injection,
   serialization/file uploads, credential lifetime and logging.
4. Distinguish missing controls, actual reachable exploit paths, mitigations
   already enforced elsewhere, and uncertain concerns needing reproduction.
5. Correlate with relevant **OWASP ASVS 5.0.x** verification requirements,
   but do not claim full ASVS certification from a code diff. NIST SSDF
   supplies lifecycle-level practices, not individual exploit proof.
6. Write minimal safe fixes and negative tests; do not execute exploit payloads
   against third-party/live systems or ask for secrets without authority.

## Report contract
Each finding: file:line/flow, reachable preconditions, violated trust boundary,
consequence, impact/likelihood reasoning, confidence, proof/reproducer where
safe, minimal fix and a regression test. Mark potential risks as hypotheses,
and accept **no findings** when no supported defect exists.

## Targeted references
- [Trust-boundary review with OWASP ASVS](references/threat-boundaries-asvs.md) —
  **read when** analyzing attacker-controlled input, authentication, object
  ownership, isolation and sensitive data flows.
- [Vulnerability patterns and safe verification](references/exploitation-paths-and-mitigations.md) —
  **read when** reviewing SQL/shell injection, SSRF, XSS, deserialization,
  secrets or constructing authorized negative tests.
- [Evidence, severity and review workflow](references/findings-and-security-evidence.md) —
  **read when** creating a security report, triaging scanner output or
  deciding if a change requires high-priority remediation.

## Boundaries
dependency-supply-chain owns artifact/dependency provenance;
external-skill-audit owns third-party agent instruction intake;
agent-tool-safety owns LLM tool authorization and injection;
git-pr-workflow owns PR collaboration. Security review complements,
but is not replaced by, SAST/DAST or passing ordinary unit tests.

## Differential security review — inspect the actual risk path

Adapt Trail of Bits' differential-review and audit-context-building:
understand behavior and assumptions first, then analyze the changed
attack surface with explicit source-to-sink evidence. Do not turn every
small PR into a multi-agent security audit.

| Level | Procedure | Evidence |
|---|---|---|
| LIGHT / R0 | No security boundary: inspect diff for obvious accidental secrets and changed permissions | Targeted check, no speculative vulnerability list |
| STANDARD / R1 | Inspect modified entry points, callers and validation, compare changed invariants and tests | Reachable scenario, impacted contract, negative oracle |
| DEEP / R2 | Prioritized threat model, relevant git history, trust-boundary paths, privilege/tenant checks, replay and fail-open behavior | Independent findings, safe reproduction and explicit coverage gaps |

**Pre-analysis:** identify who controls entry points, which principal
performs actions, sensitive assets, implicit caller guarantees, external
sinks and relevant existing guards. Separate source code behavior from
unverified architectural diagrams; use codebase-archeologist only when
genuine unfamiliarity justifies its context cost.

**Differential pass:** identify removed checks, new privileged operations,
changed default configurations and transitive callers. Inspect git
history selectively where removed security code could be a regression.
File count is not risk: a one-line removal of a tenant predicate can
be R2, while 200 localization changes are not automatically vulnerable.

**Adversarial pass:** for each hypothesis name controlled input,
preconditions, actual reachable source -> validation -> auth -> sink,
existing mitigations and safe negative test. Include status of
reproduction (confirmed, plausible, disproven, not tested). Don't
submit live payloads, disclose secrets or invent an exploit from static
appearance alone. Validate false positives before assigning severity.

**Review packet:** file:line and SHA, threat actor, asset, exploit
preconditions, impact/likelihood rationale, minimal fix, regression oracle,
required review level and what was not assessed. Security requirements are
gates: unavailable independent R2 review remains BLOCKED; reducing cost
does not waive known vulnerabilities. Agent tool permissions belong to
agent-tool-safety rather than ordinary web code review.
