# LLM production verification and rollout

**Read when:** determining whether a prompt/model/gateway/agent is safe to release or comparing native/provider abstraction.

## Layered tests
1. **Unit adapter**: fake SDK success/refusal/429/5xx/toolUse/invalid schema/cancellation/partial stream; no real model spend.
2. **Contract integration**: authorized staging credentials, supported model ID/region, tool selection and complete response parsing, usage metadata and quota behavior.
3. **Deterministic safety**: JSON schema, access denial, tenant scoping, tool allowlist, idempotency and deadline.
4. **Evaluation**: frozen representative labeled tasks with hidden edge cases; compare accuracy, refusal correctness, hallucination, precision/recall where defined, human rework and token cost.
5. **Operational rehearsal**: overload, provider outage, fallback region failure, streaming cut and manual replay; observe dashboards/alerts.
6. **Canary/rollback**: version model, prompts, SDK dependencies and provider policy; deploy with rollback conditions.

## Quality metrics must have denominators

Schema validity = valid outputs / attempted outputs, including timeouts separately. Task success = accepted outcomes / labeled attempted tasks. Cost per completed useful task can matter more than raw model token price. p95 latency includes queue time and retries, not just model API processing.

Use multiple runs for nondeterminism and report confidence/limitations. LLM-as-judge needs a documented rubric, bias checks and human spot validation. Never claim deterministic quality because temperature=0.

## Evals by workflow type

- Extraction: exact-field validity, missing data abstention, PII exclusion and source grounding.
- Customer FAQ/RAG: citation faithfulness, retrieval recall, knowledge freshness and refusal for unsupported claim.
- Tool agent: authorized tool selection, arguments, retry dedupe, malicious tool-output resistance and rollback.
- Multi-provider: ability parity, token budget, finish reasons, structured output support and safety behavior.

## Prohibited shortcuts

Test only happy-path prompts, unreviewed live production canary on customer data, logs raw prompt in public telemetry, automatic fallback that violates data residency, assumed provider price/token equivalence.

Official: https://docs.langchain.com/oss/python/langchain/structured-output and https://docs.litellm.ai/docs/python_sdk and https://www.nist.gov/itl/ai-risk-management-framework .
