# Adaptive engineering methodology — planning, execution, review and cost

This document specifies the cross-skill **behavioral contract** for
Agent Engineering Toolkit. It improves methods inspired by
obra/superpowers, but does not import its complete framework, hooks
or automation engine.

## Principles and source boundaries

Reference upstream: obra/superpowers, reviewed at
bb92a77741419a4ab5f06e711a283343f1ada0c3 (2026-10-10).
Licence: MIT. This change is **an original adaptation of concepts**,
not a verbatim copy of upstream skills or scripts. Upstream provides
deep planning, task handoffs, self/independent reviews, worktree safety,
ledger recovery and merge choices. AET deliberately maintains its own
portable, selective skill taxonomy and explicit authorization boundary.

No new persona was created. implementation-planning is a new Core skill
because plan authoring is independently useful; methods for parallelism,
execution, reviews and worktrees extend existing owners rather than
duplicating them. Source content is treated as untrusted; no upstream
hook/script was executed during source inspection.

## Three independent decisions

| Axis | Modes | Owner |
|---|---|---|
| Execution rigor | LIGHT, STANDARD, DEEP | task-routing + workflows |
| Review assurance | R0 self, R1 targeted independent, R2 deep risk-led independent | task-routing + verification-before-done |
| Delivery topology | inline, subagent-driven, parallel independent domains | execution-orchestrator |

Default combinations:
- LIGHT/R0/inline for reversible local edits;
- STANDARD/R0 or R1/inline for routine feature work;
- DEEP/R2/inline or delegated for security, data integrity and
  irreversible effects, with independent gate verified or BLOCKED.

Do not select by LOC or keywords. A single-line access-control change
can be DEEP/R2. A large generated metadata update may be STANDARD/R0.
Review *depth* is not review *model count*: one qualified independent
reviewer can cover both spec adherence and quality if evidence is sufficient.

## Adaptive process in order

1. Inspect actual user constraints, impact, reversibility, dependencies,
   available tools, existing tests and current repo state.
2. Route to minimum safe rigor/review without interpreting a keyword
   as an authorization or native skill activation.
3. Prepare a proportionate implementation plan only when decomposition
   improves correctness; include producer/consumer contracts and negative
   acceptance on nontrivial tasks.
4. Execute inline by default; optional subagents get a focused brief
   and explicit allowed paths. Parallelize independent work only after
   resource and interface overlap analysis.
5. Verify incremental behavior with real test outputs, preserve ledger
   when resume/compaction warrants it, and inspect complete BASE..HEAD.
6. Apply R0/R1/R2 based on observed risk; adjudicate concrete reviewer
   findings with bounded re-review and regression tests, not consensus.
7. Check combined current revision, branch/PR permissions, skipped
   evidence and human approval. Never auto-merge or auto-deploy.

## Cost and correctness measurements

Scenario baseline: no toolkit or prior toolkit variant. Treatment:
adaptive skills installed in the same host, same task, code revision,
model/runtime conditions and available tools. Measure where possible:
actual tokens, context loaded and reference reads, number of agents
and review calls, elapsed time, accepted regression cases, escaped
defects, risky approval violations and human corrections. If real
tokens cannot be extracted, use character-count **proxy** clearly
labeled as such, not fabricated token costs. Re-run on held-out tasks
including low-cost simple edits and high-consequence one-line fixes.
The eval fixtures are specifications, **not observed successes**.

## Coherence and governance

New source belongs in this toolkit's existing categories. No new
agent persona is necessary: execution-orchestrator and
review-feedback-arbiter remain opt-in. The new Core planner is not
installed in minimal by default; curated engineering profiles may
include it when multi-step implementation is frequent. Discovery via
registry does not itself activate a skill in Claude, Codex or another
host. Verify actual native installation and routing separately.

References are loaded only for the relevant branch:
- implementation-planning: task plan, dependencies, risk focus;
- task-routing: adaptive review choice;
- git-pr-workflow: worktree, review packet, branch finish;
- verification-before-done: evidence quality and review independence.

## Known limits

This is a **documented and deterministically tested method**, not proof
that every agent follows it, that live Code/Claude tools are available,
or that the outcomes equal or exceed Superpowers across real tasks.
Behavioral held-out A/B tests and real native host traces are separate
acceptance gates. Do not claim budget savings, quality superiority,
automatic reviewer dispatch or production readiness without evidence.

## Optional deterministic policy example

The pure Python advisory uses structured observations, not untrusted keywords. It never dispatches, authorizes, edits files or substitutes for task-specific judgment:

~~~python
from toolkit.adaptive_policy import ChangeSignals, assess

change = ChangeSignals(
    local_reversible=True,
    authorization_or_secrets=True,
    reviewer_available=False,
)
decision = assess(change)
assert (decision.workflow, decision.review, decision.execution) == ("deep", "R2", "inline")
assert "independent R2 risk review unavailable" in decision.unmet_gates
~~~

A high-impact change with an unavailable reviewer remains implementable in an authorized development environment but **cannot be reported as independently reviewed**. The decision.ready_for_integration property only summarizes known missing gates; it does not grant merge/deploy authorization or establish complete real-world safety.

## Research-driven deepening

Fourteen existing skills now include proportional execution methods sourced from a pinned review of recognized public GitHub repos: debugging/TDD/discovery, paired skill evaluations, differential security review, safe tool authorization, preflight deployment and compact codebase handoff. See [source and adaptation decisions](methodology-source-review-2026-10.md). These additions do not prove native model adherence or quantified savings; inspect [unexecuted behavior scenarios](../evals/methodology-depth.yaml) and use the offline [paired-observation summarizer](../scripts/summarize_skill_evals.py) only for trace-backed native runs.
