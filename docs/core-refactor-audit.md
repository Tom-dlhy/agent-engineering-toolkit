# Core category refactor — governance audit and uniform quality contract

Date: 2026-10-11. Scope: `skills/core/` only, plus the **cross-cutting** registry,
validator, evaluation fixtures and documentation needed to enforce one standard.

## Charter-aligned decisions

| Existing skill | Audit finding before this PR | Decision and implementation |
|---|---|---|
| `task-routing` | ~1.2 KB routing summary, no local leaves; lexical ranking could be mistaken for authority | **EXTEND**: explicit impact/rollback/workflow decisions; skills, installed profile and context cost; 2 leaves |
| `systematic-debugging` | ~1 KB checklist, no causal diagnostics, concurrency/flaky evidence | **EXTEND**: evidence ladder, reproducibility, falsifiable hypotheses and regression methodology; 2 leaves |
| `verification-before-done` | ~1.1 KB checklist, limited cross-environment proof/release semantics | **EXTEND**: claim-to-proof matrix, statuses, stale CI, authorization boundary; 2 leaves |
| `skill-authoring` | ~1.6 KB methodology plus obsolete instruction to assign different maturity levels | **EXTEND**: duplicate/overlap decision protocol, single quality contract, provenance and eval plan; 2 leaves |
| `requirements-discovery` | Already actionable, with two substantial leaves; could be confused with compulsory questioning | **EXTEND central router**; preserve the two well-scoped leaves, reinforce ask-only-if-blocking |
| Separate sixth Core skill | No distinct responsibility justified | **REJECT/DEFER**; keep 5 skills, no extra profile installation |

## Single quality acceptance standard

All skills in the catalog use one standard: precise task trigger/exclusions,
actionable SKILL.md, decisions/alternatives, domain-appropriate depth, error/
security bounds, validation, negative scenarios and responsible provenance. A
technical specialist needs enough local technical substance for routine work;
methodological skills can be shorter when their *method itself* is complete.

**No per-skill maturity fields, ranks or expert badges in the registry.**
The optional `version` field in SKILL.md means document/API revision, not quality.
Discovery/Activation/Reference are three **context-loading** stages.
Light/Standard/Deep are three **execution workflow** modes. Neither axis
establishes trustworthiness, correctness or priority of a skill.

## Structural validator changes

- Removed the old **opt-in** validation branch that only checked deep leaves
  for entries carrying a maturity value (66 historical fields).
- The same path-allowlisting, symlink rejection and heading/read-condition checks
  now apply to **every declared reference** in all 113 skills.
- Fail validation if a future entry reintroduces a `maturity` key.
- Validate keyword type/nonempty contents and duplicates uniformly.
- No fixed minimum count of leaves for every skill: this would artificially
  fragment methodological skills and contradict charter section 8.
- Structural checks cannot assess actual expert correctness. Missing behavioral
  and real-environment evidence is an open acceptance item, not a maturity rank.

## Routing and behavior evidence

`evals/core-routing.yaml` lists positive, negative/neighbor and workflow-mode
scenarios. The deterministic `tests/test_core_governance.py` validates lexical
selection against these fixed fixtures, selective reference paths, absence of
old maturity metadata, a malformed-reference fixture without any special labels,
and context-budget/installation boundaries.

The router is **lexical and advisory**. These tests do not demonstrate that
Claude/Codex automatically invoke the correct skill in a real project; that
requires explicit host-level evaluation with recorded commands and prompts.

## Non-negotiable operational boundaries

- Code from untrusted repositories or skill docs is not automatically run.
- A user asking for a review does not authorize merge, deployment, network
  side effects, credential escalation or destructive operations.
- An uninstalled catalog skill is not magically available to a host.
- Asking a user to repeat known constraints is not requirements discovery.
- A CI green status on an older revision is not proof for a new commit.
- An agent diagnosis without a reproduced/disproved mechanism is a hypothesis.

## Future category refactors

This PR does **not** claim every technical skill has completed its content audit.
The remaining domains are evaluated against exactly the same checklist, with
gaps tracked by concrete tests/examples and scope, **not ranked status**.
In later domain PRs, add representative executable exercises and real-agent
behavior measurements in addition to structural validation.

Governance source: the user-maintained *Charte de gouvernance et d'évolution —
Architecture arborescente et expertise progressive, v2*, sections 1–9.
