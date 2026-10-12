---
name: task-routing
domain: core
version: "1.0.0"
description: >-
  Use when determining which installed skills and Light/Standard/Deep workflow,
  R0/R1/R2 review level and execution strategy fit a task with uncertain scope,
  risk or tooling. Do not force deep planning, subagents, independent review or
  broad reference loading on a straightforward reversible change.
---

# Task routing — the least expensive workflow that adequately controls risk

## Role and limits

This skill selects **rigor**, **review effort** and **knowledge to load**;
it does not approve destructive actions, invent available subagents, perform
implementation or declare completion. An agent should choose **one** primary
skill and at most the additional independent specialists required by the task.
LIGHT/STANDARD/DEEP describe execution intensity; Discovery/Activation/Reference
describe knowledge loading; R0/R1/R2 describe review effort. These are related
but different axes. A small code diff can need deep review, and a large
mechanical diff can need only routine checks.

## Step 1 — gather observed signals, not just keywords

Inspect user goal and explicit constraints, existing tests, touched contracts,
target repo conventions and approved side effects. Identify:
- **Impact:** cosmetic/internal, public interface, permission boundary,
  production data, payment, credentials, infrastructure or availability.
- **Change topology:** local independent edit versus shared schema/callers,
  migration, cross-component behavior or external services.
- **Unknowns:** clear reproduction/oracle, missing input, new design decision,
  existing failures and compatibility uncertainty.
- **Reversibility:** revert isolated commit versus data loss, propagation
  to consumers, irreversible writes or multi-stage rollback.
- **Evidence:** existing automated tests, realistic fixture, external host
  dependency, actual reviewer/subagent tool availability.
- **Permissions:** an explicit approval for merge/deploy/delete is distinct
  from an approval to implement source changes.

Do not delegate this decision to toolkit.catalog or a keyword classifier.
The finder returns candidates, never a workflow verdict. For "production"
in a CSS documentation sentence, inspect the real change before choosing LIGHT;
for a one-line tenant lookup restriction, inspect the authorization boundary
before choosing DEEP. If facts are unavailable, describe the uncertainty rather
than claiming the task is safe.

## Step 2 — choose the minimal safe workflow

| Evidence | Mode | Default process |
|---|---|---|
| Local, reversible, acceptance obvious, no relevant shared contract | LIGHT | Direct edit; one targeted check, R0 |
| Multiple components or new behavior, ordinary recoverable risk | STANDARD | Brief plan, verify incrementally; R0 or R1 based on review trigger |
| Authorization/secrets, migrations, sensitive data, irreversible effect, weak recovery or high uncertainty | DEEP | Explicit risk/approval gates, detailed plan, negative tests, independent risk review when required |

Classify on the highest-consequence change, not by task word count. Escalate
one dimension when an actual signal appears; de-escalate after evidence removes
the concern. Do not keep DEEP just because planning happened to be long.
Hard permission gates cannot be de-escalated.

## Step 3 — assign review level separately

- **R0 / self-review:** default when an isolated diff has a reliable
  automated or manual oracle. Inspect full own diff for accidental scope;
  run the targeted test/check and report limitations.
- **R1 / targeted independent review:** select when unfamiliar code,
  multiple changed contracts, complicated regression surface, conflicting
  evidence or consequential ambiguity makes a fresh reviewer worthwhile.
  Review the changed slice and interface callers, not the whole repository.
- **R2 / deep risk-led review:** select when authorization, sensitive data,
  migrations, destructive operations, serious race/replay exposure or
  high-consequence regression requires separate requirement/compliance and
  code-quality/security scrutiny. These are **review concerns**, not a
  mandatory count of subagents: one qualified reviewer can cover both when
  evidence and independence are sufficient.

Independent review is conditional on tools/budget **except** when a required
policy or safety gate cannot be met otherwise: then record BLOCKED and do
not assert merge/deploy readiness. Failed checks invalidate "review passed"
until the exact corrected revision has been retested. Never spawn a reviewer
solely because a small edit was committed.

## Step 4 — choose executor economics

Inline is the default, especially with no subagent tool. Use a fresh implementer
for complex independent tasks when reduced context contamination outweighs
startup cost; dispatch a separate reviewer when R1/R2 calls for fresh judgment.
Parallelize only proven independent investigations or isolated tasks with
frozen interfaces and separate workspaces; shared types/files/DB migrations
typically serialize. Track delegated tasks and cost; do not claim parallel
execution just because there are multiple task headings.

A longer session may need a resumable file-backed ledger even when inline.
The ledger is overhead justified by compaction/retries, not a mandatory file
for LIGHT. Cost includes tokens, duplicated repo reads, agent startup, tool
calls and reviewer rounds **and** cost of escaped defects.

## Step 5 — progressive discovery and escalation

Read metadata for candidate installed skills first; check positive and
negative triggers. Host-exposed names/descriptions are the first choice; when
the host does not expose enough, request a small explicit profile catalog via
`python scripts/skillctl.py routing-context --profile minimal` in an AET
checkout. The YAML reports AET architecture and metadata of only the chosen
profile (or explicit skills), not the entire library. It does not install or
activate skills. Compare candidates by actual task intent and repository
context; select one primary skill, genuinely orthogonal helpers, or NONE.
Load their SKILL.md, then specific local references on observed need.
Avoid blindly opening whole reference trees or loading a persona to fix
a simple syntax bug. An uninstalled skill's registry entry does not imply
the host automatically activates it. Escalation triggers: observed test
failure, security boundary discovery, irreversible side effect, new public
API, widened file scope, conflicting agent outputs or uncovered risk;
record why and what new proof is required.

## Decision examples

1. Correct documentation spelling: LIGHT / R0 / inline, no plan file.
2. Add a recoverable UI form with backend endpoint: STANDARD / R0 with
   effective tests, or R1 if cross-component contract review adds value.
3. One-line cross-tenant authorization change: DEEP / R2 despite tiny diff.
4. Investigate three unrelated failing suites: parallel investigations only
   if interfaces/resources disjoint; one integration check afterward.
5. Refactor 20 isolated generated descriptions: STANDARD / R0 if deterministic
   tests cover all changes; size alone is not deep-risk evidence.

## Selective references

- [Risk, workflow and escalation](references/risk-workflow-triage.md)
  — **read when** selecting risk gates, irreversible effects or rollback.
- [Skill routing, exclusions and context budget](references/discovery-and-context.md)
  — **read when** candidates overlap or references may inflate context.
- [Adaptive review and execution decision procedure](references/adaptive-rigor-and-review.md)
  — **read when** deciding R0/R1/R2, subagent cost or escalation from evidence.

## Handoff to other owners and exit

implementation-planning writes the multi-step plan; execution-orchestrator
coordinates it; git-pr-workflow manages branch/PR; review-feedback-arbiter
adjudicates actual feedback; verification-before-done checks final evidence.
Report the chosen workflow, review level, executor, selected skills and
rejected costly alternatives when non-obvious, tools unavailable, and the
first falsifiable check. Never use a heuristic result as authorization.

## Research-backed selection: route the task, not vocabulary

Adapt the comparative skill-selection approach of Anthropic skill-creator and GitHub's curated agent-skill-stack concept. The lexical search rank is a candidate list, never proof of correct activation.
The agent (not Python) owns skill choice and workflow/review judgments. Only
explicit caller-reported structured change signals can be evaluated by
`toolkit.adaptive_policy.assess`, and even those are not verified facts.
The legacy `suggest_workflow()` API abstains with `unclassified` for free text.
No skill selection grants permission to commit, merge, deploy or delete.

1. **Cheap shortlist:** from host-visible installed metadata, or scoped `routing-context` YAML when useful, identify up to three plausible candidates and include NONE. Compare positive and negative activation triggers and the actual project stack. Treat multilingual/paraphrased intent as a reasoning problem, not a requirement to add synonym rules to Python. A match on "base" must not confuse Base UI with a database.
2. **Bounded evidence:** inspect impacted files, requested artifact and contract ownership for only the shortlist. Decide the workflow from consequential changes (for example payment writes, tenant isolation, migration rollback and irreversible deletion), not words in documentation. Pick one PRIMARY skill and only truly orthogonal SECONDARY specialists. No repository-wide skill-body scan.
3. **Activation evidence:** identify whether the host actually exposed and loaded the selected skill. A registry hit is not native activation; an absent subagent tool must not be invented.
4. **Dynamic reassessment:** reroute on observed new dependencies, authentication boundaries, irreversible effects or failed tests. De-escalate if actual change is harmless copy, while preserving any mandatory approval.

| Request | Wrong shortcut | Evidence-led route |
|---|---|---|
| Documentation typo on a production page | DEEP from keyword production | LIGHT/R0, no review agent |
| Tenant B reads tenant A's ID | LIGHT from one-line patch | DEEP/R2, authorization specialist |
| Base UI Select | Database selection from base | UI provider skill |
| Intermittent pytest | Test-adversary for every failure | systematic-debugging and flaky methodology |
| Improve agent answer quality | llm-integration by default | llm-evaluation for measured experiments |

For changed triggers create positive, negative, ambiguity and multilingual examples. Offline lexical rank tests only assert rank. Native tests must separately record skill actually loaded, references consumed, task success, false activation and tokens **only when host telemetry exists**. Compare the old skill against the modified one; false activation and wasted R1/R2 reviews are regressions. Never claim actual agent routing was measured from YAML fixtures.
