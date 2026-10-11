---
name: task-routing
domain: core
version: "0.2.0"
description: >-
  Use when determining which installed skills, reference leaves and Light/Standard/Deep
  execution workflow fit a software task with uncertain scope or risk. Do not force
  orchestration, installations or Deep workflow onto clearly localized edits.
---

# Task routing — select the least expensive safe execution path

## Scope and inputs

Inspect user intent and explicit constraints, target repository conventions, available tools,
skill **descriptions** and installed profile before reading skill bodies. The registry is
a catalog, not a native auto-invocation guarantee; do not assume uninstalled skills are
available. User authorization and higher-priority project rules override suggestions.

## Decisions in order

1. **Understand the outcome:** classify the requested change and what must be demonstrated.
   Distinguish a known implementation request from optional discovery, a bug, and a request
   for a plan. Never re-ask facts already present in conversation or repository.
2. **Triage impact:** examine affected files/interfaces, data sensitivity, deployment surface,
   destructive/irreversible side effects, rollback difficulty and uncertainty.
3. **Choose workflow:** LIGHT for local reversible work with targeted verification;
   STANDARD for ordinary multi-file changes; DEEP when the *actual change* crosses
   security, external effects, production-data, migration or high-risk architecture boundaries.
   A keyword or advisory `suggest_workflow()` is not authority: adjust based on evidence.
4. **Match skills to responsibilities, not technology names alone:** start with one primary
   skill (often no specialist on a tiny edit), add the smallest number of independent
   specialists when the task genuinely crosses boundaries. Compare positive and negative
   activation conditions; lexical ranking is only a candidate list.
5. **Load progressively:** discover metadata → read selected SKILL.md → explicitly choose
   only relevant local reference leaves. Do not recursively open a whole domain or install
   all candidate skills; explicit installation is a separate user-authorized operation.
6. **Reassess during execution:** if new evidence changes risk, expand checks and consult
   the relevant specialist; do not restart the entire workflow automatically.

## Practical examples

| Request | Initial route | Do NOT do |
|---|---|---|
| Fix one confirmed typo | LIGHT, perhaps no additional skill | Ask architecture questions or launch subagents |
| A 500 error with unclear cause | systematic-debugging, LIGHT→STANDARD as evidence grows | Guess an error cause from lexical similarity |
| Public REST endpoint change | fastapi-service plus test strategy if needed, STANDARD | Load every Python and cloud skill |
| Production schema backfill | schema-migrations, DEEP with rollback and staging checks | Treat `migration` keyword as user approval to deploy |
| Compare two technical approaches | technology-tradeoffs / architecture-decision | Demand an implementation branch prematurely |

## Selective reference routing

- [Risk, workflow and escalation](references/risk-workflow-triage.md) — **read when**
  determining blast radius, interruption policy, irreversible effects, escalation or rollback.
- [Skill routing, exclusions and context budget](references/discovery-and-context.md) —
  **read when** comparing overlapping skills, routing ambiguous tasks, checking profile
  availability or measuring selective reference use.

## Boundary with other Core skills

`requirements-discovery` is a requested clarification interview, not mandatory task triage;
`systematic-debugging` diagnoses a failing behavior; `verification-before-done` checks
evidence before claiming completion; `skill-authoring` governs actual catalog changes.

## Exit evidence

Name the chosen workflow and why, the selected skill(s) and rejected adjacent candidate
when ambiguity matters, references actually read, and required verification. Report absent
tools or permissions; never infer skill activation from a YAML match.
