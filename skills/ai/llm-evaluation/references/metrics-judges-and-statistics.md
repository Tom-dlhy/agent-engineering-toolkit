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
