# Metrics, calibrated judges and statistical uncertainty

**Read when:** comparing prompts/models, using LLM-as-a-judge
or claiming a measurable gain with repeated stochastic calls.

## Metric definitions by outcome
- Deterministic: required JSON schema, tool name/arg structure,
  runtime authorization, forbidden network call, grounded citation.
- Quality: task correctness, helpfulness, supported claims,
  abstention precision/recall for unanswerable tasks.
- Operational: p50/p95/p99 latency including retries, cost per
  *successful useful task*, timeout/cancellation, usage tokens
  when provider reports them.
- Safety: unauthorized side effects, privacy leaks, unsafe
  completion under adversarial instructions.
Never substitute low temperature for determinism evidence.

## LLM judge calibration
A model judge may have position, verbosity, familiarity or
self-preference bias. Blind output ordering, hold rubric and
gold labels constant, sample disagreements, calibrate against
human raters. Use executable checks whenever machine-verifiable
rather than judge reasoning ("the code compiles" -> run it).

## Comparison statistics
Use paired cases across candidate and baseline to reduce
variance; repeat calls when stochastic. For proportions,
report numerator/denominator and uncertainty intervals,
avoid tiny-sample "win by 2%" claims. If testing many prompts
on same holdout, control false discoveries and explicitly
state selection bias. Higher average score can hide a
critical regression in a minority slice.

## Decision report
Show overall, slice/critical fail, variance, cost/latency,
sample count, model versions/settings, evaluator revisions,
nonblind caveats and rollback triggers. Qualitative examples
help understand errors but are not independent evidence.

Sources: https://platform.openai.com/docs/guides/evals ,
https://platform.openai.com/docs/api-reference/graders .

## AET paired skill-evaluation protocol (research-informed)

**Read when:** a skill prompt, routing rule or method has changed and the maintainer needs to demonstrate improved engineering outcomes or reduced cost.

**Source inspiration:** Anthropic skill-creator uses old-versus-new skill pairs, a baseline run, task-level expectations and blind output comparison. This is a methodological adaptation; Anthropic's scripts and subagents are not vendored.

### Dataset and evidence inventory

Build a manifest before touching the candidate:
- task_id / task prompt / input artifact hashes / accepted success oracle;
- baseline skill SHA / candidate skill SHA / host and model IDs;
- allowed tools, network scope, required approvals and prohibited actions;
- expected activation decision, negative/no-skill neighbor case;
- grading procedure and reviewer independence;
- resource budget: runs, tool calls, tokens if observable, time.

Use one representative fixture per common path and at least one ambiguous,
unsafe and very small LIGHT example. The **negative activation** case is
crucial: a skill that improves hard tasks but activates unnecessarily
for typos can make the toolkit more expensive. Do not expose held-out
answers to the agent whose outputs are being evaluated.

### Run matrix

| Variant | Instructions | Same input and tool surface? |
|---|---|---|
| Baseline | Frozen previous skill for an improvement experiment | YES |
| Treatment | Exact candidate skill SHA | YES |
| Optional no-skill control | No specialist, when comparing usefulness at all | YES |

Pair at the same time/under comparable host conditions where possible.
Run repeated trials for nondeterministic models, record actual sample
size and variability. If tools differ, disclose that results are not
strictly comparable. Failures due to environment are NOT_RUN/BLOCKED,
not silently removed from denominator.

### Grade artifacts, not confidence

First use independent deterministic assertions: valid file, targeted
test outcomes, correct access denial, no unintended writes, task completion
and actual skill loading. For subjective writing/architecture review,
blind A/B compare without revealing model identity and calibrate on a
small expert-labeled sample. Ask graders to identify weak or vacuous
acceptance tests. A judge saying "looks good" cannot make a failing
test pass.

Compute per task group: acceptance pass rate, critical violations,
false skill activation, reviewer/subagent count, actual tokens when
available, latency distribution and cost per successful task. Report
paired differences with denominator, confidence/variance and outliers.
Label character-count-based token proxies prominently. Do not publish
"35% savings" if no host telemetry supports it.

### Promotion example

Candidate saves 12% median wall time over eight paired tasks but one
tenant-isolation case fails that previously passed: **NO GO** despite
lower cost. If both pass and cost is unobservable, claim quality parity
in these fixtures only; do not claim token savings. Open a separate
authorized host run before asserting native Codex/Claude behavior.

Official method reference:
https://github.com/anthropics/skills/tree/main/skills/skill-creator
