# Security review — evidence, severity and developer handoff

**Read when:** writing a security review with actionable findings, severity,
root cause and validated fixes, or triaging automated scanner alerts.

## Finding format
ID, location and relevant caller/sink, trust boundary, attacker capability,
preconditions, effect, severity rationale, confidence, proof in authorized
environment, remediation, regression test and residual risk.

### Example (hypothetical, not a finding in this repository)

~~~text
SEC-004 | HIGH | app/routes/documents.py:74
Entry: GET /documents/{id}; valid tenant-B token + tenant-A document ID.
Behavior: select_by_id(id) without tenant filter, response returns record.
Impact: cross-tenant document disclosure.
Evidence: authorized negative integration test demonstrates 200 where
403/404 expected.
Remediation: apply tenant predicate in trusted repository layer,
check result ownership; cover list, export and mutation routes.
Retest: direct IDs, guessed IDs, cached response and bulk export.
~~~

Severity depends on exposure and sensitive data, not a raw OWASP category.
Document whether exploit is confirmed, probable, or requires manual proof.

## Scanner findings are hypotheses until triaged

SAST catches vulnerable patterns but may miss domain authorization and supply
false positives. DAST tests reachable behavior but doesn't guarantee all
paths were exercised. Dependency CVEs describe publicly known package
issues and may require reachability/exposure analysis. Manual review should
neither rubber-stamp nor dismiss scanner output without evidence.

## Reproduction safety

Do not use real production credentials or enumerate other tenants without
authorization. Prefer test fixtures, synthetic accounts and a disposable
environment. Record sanitized evidence that demonstrates failure without
publishing exploit payloads/customer data unnecessarily.

## Triage

| Priority | Rationale | Immediate step |
|---|---|---|
| Blocker | Unauthorized sensitive write/read with demonstrated reachability | Block release, remove exposure, fix |
| High | Credible high-impact exploit path with few preconditions | Prioritize targeted reproduction + fix |
| Medium | Valid control weakness with constrained exploitability | Track, test, remediate |
| Low / informational | Defense-in-depth, speculative/inapplicable control | State limitation; avoid alarmism |

Use project-specific severity policy / CVSS where applicable, but
not arbitrary confidence disguised as an exact score.

## Completion

An honest "no confirmed finding" is acceptable. Give changed files,
tested threat paths, test results and any unknown areas; it does not mean
system fully secure or ASVS-certified.

Official source: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
and https://owasp.org/www-project-application-security-verification-standard/ .
