# Technical selection — evidence, disqualifiers and comparison matrix

**Read when:** evaluating a library, database, managed service,
framework or buy-vs-build choice under real constraints.

## Separate hard requirements from preferences

Hard requirements: approved region/residency, license, supported
runtime/API, provider security requirements, compliance and
budget ceiling. Disqualify infeasible candidates first.
Preferences: ergonomics, migration effort, operational burden,
feature completeness, ecosystem support, cost and portability.

| Criterion | Weight (example) | Candidate A | Candidate B |
|---|---:|---|---|
| Data residency (must) | Gate | Pass with evidence | Unverified → blocked |
| Team experience | 2 | Proven | Training required |
| Provider feature fidelity | 3 | Native | Abstraction gap |
| Operation/on-call cost | 3 | Existing service | New gateway/DB |
| Migration reversible | 2 | Low coupling | Major state cutover |

Numeric weights shown are **illustrative**, not scientific truth.
Score only known evidence and report gaps. Never convert an
unsupported rumor into a 9.5/10 score. A simple candidate with
reasonable functionality can dominate a theoretically more
advanced tool after setup and incident costs are included.

## Reliable evidence

Prefer official release notes, support/compatibility matrix,
standards, licensing text, security advisories and actual code.
Community Stack Overflow answers can show edge cases but are
version/context-dependent. Benchmarks must use comparable
hardware, load, dataset, config and failures. Verify current
pricing/entitlements at time of decision with an official source.

## Anti-patterns

One-option "comparison", stars as security proxy, benchmark cherry
picking, inventing throughput per user, declaring managed services
always cheaper, assuming open source implies permissive license,
ignoring constraints already supplied by user.

## Decision handoff

Give default, credible runner-up, rejected alternatives,
tradeoffs and one experiment that would change the choice.
Use architecture-decision ADR for major irreversible
organization/architecture changes.

Sources:
https://learn.microsoft.com/en-us/azure/architecture/guide/ ,
https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html .
