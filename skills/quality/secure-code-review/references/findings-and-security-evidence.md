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

## Differential vulnerability review and false-positive triage

**Read when:** reviewing an authorization or security-relevant diff,
especially where changes affect callers, defaults or dataflow.

### Three passes, limited by actual risk

**Pre-analysis:** confirm exact base/head SHA, entrypoints, security
identities and trust assumptions. A raw source snippet cannot prove
reachable behavior. Map the first and second hop of affected callers
where necessary, including a potentially unaware background worker.

**Diff analysis:** inspect the changed lines, removed guards, new
external effects, callers, tests and relevant git blame for code that
may have prevented a known vulnerability. Estimate blast radius from
actual call sites; do not invent a numeric count from a partial grep.
A small diff that weakens authorization is high consequence even if
only one line changed.

**Adversarial hypothesis:** trace input -> validation -> auth ->
sensitive sink. State attacker capability, current effective guard,
reproduction preconditions, test or instrumentation, impact and
confidence. If an existing control blocks the path, downgrade or
reject the finding with evidence; no performative "security problem"
labels for speculative issues.

### Report contract

| Field | What counts as evidence |
|---|---|
| Location | File:line and candidate revision |
| Reachability | Caller/input and authorization context |
| Consequence | What a reasonable user/attacker obtains |
| Proof | Safe failing test, trace, or explicitly marked hypothesis |
| Fix | Smallest correct defense at trust boundary |
| Validation | Negative regression, tests on fixed current HEAD |
| Limits | Interfaces, platforms, tenants or versions not checked |

Deep R2 changes require independent reviewer where prescribed;
R1 is scoped; R0 self-review remains reasonable for nonsecurity
cosmetic diffs. An automated scanner can assist but cannot alone
certify non-exploitability.

Source inspiration:
https://github.com/trailofbits/skills/tree/main/plugins/differential-review
