# LLM release gates, online QA and rollback

**Read when:** deploying changed prompt, model revision,
provider route, agent graph or safety policy to users.

## Release protocol
1. Freeze baseline and candidate model/prompt/settings, tools,
   corpus/retriever revision, schemas, region and budget.
2. Run functional tests and held-out cases with paired
   comparison and security/denial challenge cases.
3. Define blocking thresholds before candidate inspection:
   zero known severe unauthorized actions in test suite,
   no schema regression, bounded p95/unknown timeouts,
   domain-specific accepted accuracy and abstention.
4. Canary for approved traffic segment with privacy-safe
   telemetry, separate assignment and opt-out considerations.
5. Compare end-user task success and correction burden,
   not only token/response counts. Revert routing/prompts/
   feature flags when agreed trigger occurs.
6. Capture incident cases for development suite; preserve
   untouched holdout for future unbiased evaluation.

## Production observability
Track selected provider/model revision, finish/refusal reason,
tool steps, attempts, schema validation errors, budget and
rate-limit rejects, user corrections and retrieval failures.
Avoid logging customer prompts/responses by default.
Probe silent wrong answers through human sampling where
consented; no perfect automated truth signal exists.

## Version change pitfalls
Provider default model alias may change; gateway fallback may
route to region/model with different safety/capabilities;
evaluation corpus may have leaked into prompt development.
A statistically better response score doesn't prove compliance
or secure tool execution.

## Limits
Real-world performance requires permitted production/staging
telemetry and human review; local smoke tests cannot certify
model quality under novel distribution or regulated uses.

Sources: https://platform.openai.com/docs/guides/evals ,
https://docs.langchain.com/oss/python/langchain/structured-output .
