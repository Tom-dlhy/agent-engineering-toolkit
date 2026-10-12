# Paired skill activation evidence (report schema 2)

`scripts/summarize_skill_evals.py --records observations.json` aggregates external
baseline/candidate records through `toolkit.skill_eval_report.compare_pairs`.
This is separate from the A/B/C engineering benchmark analyzer. It neither runs
models nor verifies that a native agent read or applied a skill. Recorded observations
and their provenance must be independently checked.

## Input and historical compatibility

Existing required fields remain: `task_id`, `variant`, `run_id`, `input_sha`,
`host`, `model`, `tool_config`, `skill_sha`, `status`, `expected_skill`,
`critical_violation`, `review_calls`. Variants are baseline/candidate; status is
PASS/FAIL/BLOCKED/NOT_RUN. Skill identifiers are nonempty strings or null.
Optional tokens/latency remain actual nonnegative host-reported measurements.

`activated_skill` can now be omitted when telemetry is missing. New optional
`activation_observed` is a strict boolean:

- `true`: the caller reports reliable observation of the activation state.
  Supply `activated_skill` explicitly; null means observed absence.
- `false`: telemetry is not reliable/available. Any recorded name remains raw data,
  but the activation metric is unknown.
- Omitted: legacy nonnull names count as **reported positive observations**, not
  independently verified evidence. A legacy null or missing field is unknown.
  A task's PASS/FAIL does not prove skill activation or absence.

Migration: keep historical records unchanged. Reaggregate them with schema 2;
only add `activation_observed: true` to a legacy null after checking a trace that
reliably demonstrates absence. Never infer this from a missing log, prompt mention,
installed skill, CLI search result or successful tests. If traces do not establish
whether a named skill activated, use false. No automatic file migration is performed.

## Categories

NOT_RUN has precedence over any activation claim. Other statuses, including BLOCKED,
use the same evidence rule: missing telemetry is unknown, while an explicitly
observed activation before blocking can still be classified.

| Expected | Observed actual | Category |
| --- | --- | --- |
| X | X | `correct_activation` |
| X | null, observation=true | `missed_activation` |
| X | Y | `false_activation` |
| null | Y | `false_activation` |
| null | null, observation=true | `correct_non_activation` |
| any | unobserved/legacy null/missing | `unknown` |
| any | status NOT_RUN | `not_run` |

Categories are mutually exclusive. X→Y is one unwanted activation, not also a
missed-absence count: absence was not observed. The single-skill schema cannot
represent multiple simultaneous activations; keep full native traces separately.

## Output changes and comparison

The report adds `schema_version: 2`, per-variant counters
`*_correct_activations`, `*_correct_non_activations`, `*_missed_activations`,
`*_false_activations`, `*_unknown_activations`, `*_not_run_activations`, and pair-level
`*_activation` categories. Category counts sum to paired tasks per variant.

The existing `*_false_activations` and pair `*_false_activation` fields now mean
**observed unwanted activation**, rather than any expected/actual inequality.
This is an intentional metric semantic correction; do not compare those counts
uncritically with schema-1 reports. `*_legacy_activation_mismatches` and pair
`*_legacy_activation_mismatch` preserve the old raw inequality for historical
comparison, including null/NOT_RUN. Raw expected/actual names, reported observation
flags and run/input/host/model/tool/skill provenance are included in each pair.
The flag records the claim even if NOT_RUN takes precedence in classification.
Old field consumers continue parsing, but must adopt the corrected meaning.

Task outcomes, critical regressions, review/token/latency deltas and comparability
checks remain unchanged. Incomplete/duplicate pairs, differing task inputs/host/model/
tool configuration/expected skill, identical run IDs or old/new skill SHAs are
rejected. Missing token/latency measurements remain null, never fabricated savings.

For a fair summary, report unknown/not-run counts and the observed denominator
alongside correct/missed/false counts. Do not hide unknown evidence in success rates
or treat it as failure. A green deterministic test suite proves this classification
contract, not native activation reliability, engineering quality or an AET gain.

Example of explicitly observed absence (merge with the other required fields):

```json
{"expected_skill": "test-strategy", "activated_skill": null, "activation_observed": true}
```

The same null without `activation_observed` is unknown. Authorization for paid
native evaluations, tests with side effects and publication remains separate.
