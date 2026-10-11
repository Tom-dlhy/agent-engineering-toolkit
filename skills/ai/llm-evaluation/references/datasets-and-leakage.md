# LLM evaluation datasets, labeling and leakage controls

**Read when:** defining evaluation cases, baselines, gold labels,
human review, holdouts or counterfactual model comparisons.

## Design a representative dataset
Define production task taxonomy first: extraction, question
answer, tool choice, refusal, multilingual, long context,
format compliance, privacy-sensitive actions and recovery.
Collect permitted/redacted examples, label expected outcome,
business severity, authorized tool list and source version.
Include genuinely unanswerable and denied-permission cases.

## Dataset partitions
Training/development cases may guide prompt design; held-out
test cases should not be repeatedly optimized against.
Document possible model memorization/contamination and
time leakage (later document in earlier question). Version
immutable evaluation manifest with hashing where permitted,
model/prompt/adapters/tool versions and human label policy.

## Independent ground truth
For deterministic data extraction gold answer may be parsed
structured fields manually verified; for open tasks require
multiple reviewers/arbitration with documented rubric.
LLM-generated gold labels without human checks are not reliable
by definition. Annotate ambiguous questions rather than
forcing an invented exact answer.

## Bias and slice design
Cover failure-important groups (rare documents, languages,
large inputs, OCR quality, adversarial cases) rather than
only typical users. Oversample severe failures for a
safety challenge set but keep a separate representative
distribution for aggregate production estimate.

## Test governance
Consent/privacy retention, data residency, audit of labeled
cases, no copied production secrets and no unaudited
recording of user prompts. Keep data accessible only to
authorized eval personnel.

Sources: https://platform.openai.com/docs/guides/evals ,
https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool .
