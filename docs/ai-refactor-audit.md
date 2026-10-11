# AI category — source-verified production engineering refactor

Review date: **2026-10-11**. Based on main after merged Core #13,
Quality #14, Architecture #15, Backend #16 and Data #17. Governance:
user-provided Agent Engineering Toolkit charter V2; *maximize available
knowledge, minimize context loaded unnecessarily*. One uniform
quality contract, **no maturity levels**, no copied untrusted scripts.

## Initial audit and decisions

| Existing skill | Gap | Decision |
|---|---|---|
| agent-tool-safety | ~1.1 KB, abstract prompt-injection warning without enforcement tests | EXTEND, 3 leaves |
| llm-evaluation | ~1 KB, no judge calibration or holdout methods | EXTEND, 3 leaves |
| llm-integration | 3 detailed native SDK references | EXTEND, fourth capability/streaming reference |
| python-llm-gateways | 3 LangChain/LiteLLM references | EXTEND, fourth DB-less budget/permission test leaf |
| rag-evaluation | ~1 KB evaluation/retrieval overlap | EXTEND, 3 ranking/citation/security evaluation leaves |

Three new specialists pass the no-duplicate check:
- **agent-orchestration**: state machine, checkpoint durability, human
  interrupt, replay; independent from gateway/library selection.
- **rag-engineering**: data ingestion/chunk/index/access/reindex lifecycle;
  independent from rag-evaluation's measurement.
- **mcp-integration**: protocol and SDK/transport/OAuth compatibility;
  separate from agent-tool-safety (which owns security *policy*).

**8 AI skills, 26 individually indexed references (20 new, 6
retained), 119 skills overall, 16 profiles**. ai-engineering
has 19 skills, python-llm-production has 20, minimal unchanged.
MCP is opt-in for Python LLM production but present in AI profile.

## Official-source verification and important corrections

| Topic | Official documentation | Supported conclusion |
|---|---|---|
| MCP latest stable | https://blog.modelcontextprotocol.io/posts/2026-07-28/ and https://modelcontextprotocol.io/specification/2026-07-28 | MCP 2026-07-28 **released**, stateless core, extensions and auth hardening; 2025 examples may be incompatible |
| MCP SDK | https://ts.sdk.modelcontextprotocol.io/ | TypeScript v1 documentation targets 2025 spec; v2 is distinct and current |
| LangGraph persistence | https://docs.langchain.com/oss/python/langgraph/persistence | Checkpointer stores thread state; Store cross-thread; InMemorySaver not restart durable |
| OWASP Agent/tool safety | https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ and https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/ | Injection, excessive agency, output handling, prompt leaks and agent security require execution-time controls |
| LiteLLM budgets | https://docs.litellm.ai/docs/proxy/users | DB-less Proxy spend limits can fail open; budgets not guaranteed by config alone |
| LiteLLM routing | https://docs.litellm.ai/docs/proxy/architecture | SDK Router vs Proxy vs native SDK, layered retries/fallback and tradeoffs |
| OpenAI API evals | https://platform.openai.com/docs/guides/evals | Evaluation sets/graders need datasets, rubrics and representative cases; grader != guarantee of task truth |
| Native AWS Bedrock | https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html | Converse/ConverseStream use typed content blocks, tool and model-specific semantics |
| Google Vertex | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling | Model suggests tool names/arguments; app enforces execution permissions |
| Azure Foundry | https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle | Model deployment/API feature capability is versioned and managed, not universal |
| Retrieval search | https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html and https://docs.llamaindex.ai/en/stable/module_guides/evaluating/ | Hybrid retrieval and reranking must be compared on same gold cases; citations/ACL separate from relevance |

**SOTA means accurate, version-sensitive, empirically testable
and policy-aware**, not asserting universal model superiority or
"100% prompt injection protection". Community Stack Overflow can
suggest reproducible issues, but primary specs/SDK references control
current-version or security-critical factual claims.

## Verifiable evidence
- **evals/ai-routing.yaml**: eight positive and seven negative-neighbor
  lexical routing examples plus no-match; lexical scores are advisory,
  NOT evidence of real host activation.
- **tests/test_ai_expertise.py**: 10 structural/routing/security/budget
  checks of registry, eight AI skills, 26 references and opt-in profiles.
- **examples/ai_security_contract/** + tests/test_ai_security_contract.py:
  nine offline Python tests: exact approval binding, tenant/tool ACL,
  schema extra argument rejection, no effect when denied and RAG
  pre-retrieval tenant filtering. **In-memory instructional example**
  only; no authentication provider, approval expiry/durable idempotency,
  production prompt injection defense or paid LLM calls.
- Existing Python/FastAPI/Node/Postgres and category suites still
  run in global CI.

## Unverified production claims and next stage
No authorized OpenAI/AWS/Vertex/Azure live paid API calls, no
actual LangGraph PostgreSQL checkpointer crash suite, no
vector search index benchmark, no real MCP client/server SDK
interoperability, no full red-team on an autonomous model,
and no cloud deployment, price/quota or live-data privacy audit.
Behavioral evaluation of Codex/Claude choosing these skills
on held-out work is still required. A green CI proves only
the explicit tested contracts and source structure.

No merge without explicit approval; PR kept Draft.
