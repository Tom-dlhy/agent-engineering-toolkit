# Stack options: hard requirements, evidence and decision matrix

Read when: recommending an end-to-end stack for an actual user workflow, or correcting a biased stack comparison.

## Intake and constraints before naming products
Record business job, target users, existing code and operations, team capability, data classifications, geography, consent/security obligations, latency/availability/restore goals, SEO/rendering, transactional invariants, integrations, budget envelope, release window and future exit constraints. Separate **user-stated** requirements, verified repo properties, unknowns and explicit assumptions. Reuse existing tech when no strong reason to migrate.

### Knockouts versus preferences
~~~yaml
scenario: private internal tool (illustrative)
must:
  - admin access cannot bypass server-side object authorization
  - audit and recoverability of persisted records
  - deployment runtime supports selected database driver
prefer:
  - low idle cost
  - comfortable TypeScript maintainability
  - minimal maintenance for solo operator
uncertain:
  - regional retention legal requirements
  - concurrency during imports
~~~
These are synthetic requirements. Reject candidate failing any genuine MUST regardless of score. Unknown on a hard gate must trigger verification, not arbitrary positive score.

## Explainable comparisons
Do not add arbitrary weighted totals for privacy/security hard requirements. For viable candidates, choose 3–6 declared weighted quality priorities (e.g. implementation effort, cost, resilience, team fluency, migration reversibility). For each score record **evidence, currency/date, confidence and what could falsify it**. Prefer qualified labels ("measured", "vendor documented", "estimated") over numeric pseudo-precision.

Illustrative matrix:
| Option | Fit | Cost confidence | Main risk |
|---|---|---|---|
| Keep existing React + Postgres + existing host | Pass | Observed billing or unknown | Operational complexity already owned |
| New serverless/edge + incompatible TCP-only driver | **Fail** | N/A | Runtime/driver mismatch; do not rank |
| New framework + managed SQL | Conditional | Estimate pending plan limits | Rewrite and migration workload |

A framework default is not automatically right for every application; user-familiar technology can be a legitimate selection factor without dictating the outcome.

## Output contract
One **preferred coherent stack**, at most two credible alternatives, disqualifiers, evidence sources, uncertainties, a shortest safe vertical-slice test and ADR trigger. No auto-generated project scaffold, package install or migration unless user specifically authorized execution.

Sources: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html and https://docs.cloud.google.com/architecture/framework and https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework
