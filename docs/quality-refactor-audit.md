# Quality category — research-backed production refactor

Review date: 2026-10-11. Project governance: Agent Engineering Toolkit
Charte de gouvernance et d'évolution, version 2.0. Scope: **all seven
existing Quality skills** after Core PR #13, with no new skill names or
maturity classifications.

## Before versus after

| Skill | Prior deficit | Decision |
|---|---|---|
| test-strategy | ~1 KB summary, no local references | EXTEND with fixtures, API contracts/E2E and property/fault testing |
| secure-code-review | ~1 KB threat list | EXTEND with OWASP ASVS trust boundaries, exploit paths and evidence |
| dependency-supply-chain | ~1 KB dependencies checklist | EXTEND with resolved graph, CI identities and artifact provenance |
| performance-profiling | ~1 KB profiling summary | EXTEND with profilers, k6/SLOs and tradeoff decisions |
| release-readiness | ~1 KB readiness checklist | EXTEND with artifact identity, migrations and progressive rollout |
| git-pr-workflow | ~1 KB git checklist | EXTEND with merge safety, PR rules and Actions trust boundaries |
| external-skill-audit | Already 2 relevant leaves | EXTEND with adversarial intake evaluation |

**19 new local leaves**, which together with the two existing
external-skill-audit leaves provide **21 indexed Quality references**.
Every skill has a narrow independent activation and three leaves.
This does **not** impose three leaves as a general catalog rule.

## Primary official research, checked during implementation

| Topic | Verified official source | Consequence |
|---|---|---|
| Python tests | https://docs.pytest.org/en/stable/how-to/fixtures.html | Isolate fixtures and clean up correctly; no universal 100% coverage |
| Browser E2E | https://playwright.dev/docs/best-practices | Prefer user-visible locators and independent tests |
| Property tests | https://hypothesis.readthedocs.io/en/latest/ | Generate edge cases, shrink counterexamples; use real independent oracle |
| OWASP review | https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html | Manual trust/logic review complements scanners |
| OWASP ASVS | https://cheatsheetseries.owasp.org/IndexASVS | Use 5.0.x relevant control families, do not claim certification |
| NIST SSDF | https://csrc.nist.gov/pubs/sp/800/218/final | Use final v1.1; later v1.2 draft not assumed stable |
| Python dependency scanning | https://github.com/pypa/pip-audit | Finds known vulnerabilities, not all malicious packages; may resolve inputs |
| CI trust | https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target | Privileged event and checkout of untrusted PR code is dangerous |
| GitHub rules | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets | Require checks/PR/reviews where configured; inspect actual repo |
| SLSA | https://slsa.dev/spec/v1.2/ | Build provenance/attestation != secure application; validate trusted builder |
| GitHub attestation | https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | Plan-dependent access/privileged permissions, not automatic across all builds |
| k6 | https://grafana.com/docs/k6/latest/using-k6/checks/ | A check alone doesn't fail run; add thresholds |
| Python profiling | https://docs.python.org/3/library/profile.html | cProfile gives time/calls, not guaranteed production throughput |

Stack Overflow/community discussions can inform debugging and point to
edge cases; version-sensitive or security-critical advice must still
be checked against upstream docs, local code and executable tests.
Sources are reference material, not commands to run automatically.

## Validation

- 7 positive and 5 negative-neighbor routing cases in
  evals/quality-routing.yaml, plus no-match examples.
- tests/test_quality_expertise.py covers all seven names, 21 references,
  path safety, uniform contract, metadata budget and repository validator.
- examples/quality_fixtures and tests/test_quality_contract_examples.py
  provide an **educational** executable in-memory check of tenant
  authorization and idempotent request replay; they are not a
  production ledger, durable DB or concurrency solution.
- All existing toolkit tests, the existing FastAPI example and budgets
  must remain green in CI before PR signoff.

## Scope and evidence limits

CI validates doc integrity, routing heuristics and deterministic Python
fixtures; it **does not** prove live ASVS compliance, valid SLSA
attestations, actual GitHub organization rules, production load capacity
or real agent skill activation. Live penetration testing, privileged
CI changes, stress tests and deployment were **not requested**.
No foreign scripts/skills/code were copied into the framework.

Quality remains seven task-scoped skills and uses the common Core
quality contract. No merge into main without explicit approval.
