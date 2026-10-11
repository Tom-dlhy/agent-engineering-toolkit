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
