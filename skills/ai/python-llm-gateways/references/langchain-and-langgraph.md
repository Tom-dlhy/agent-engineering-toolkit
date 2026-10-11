# LangChain model composition and LangGraph durable workflows

**Read when:** choosing LangChain for model/tool/retrieval abstraction or LangGraph for recoverable agent execution.

## Responsibilities

LangChain provides model initialization, message/tool schemas, structured output strategies and reusable components. LangGraph adds graph-state orchestration/checkpointers and human review paths. Neither substitutes for runtime authorization, durable external idempotency or correct cloud IAM. If task is one typed Bedrock/Gemini call, direct SDK may be materially simpler.

~~~python
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

class Extraction(BaseModel):
    category: str = Field(min_length=1)

model = init_chat_model(
    "openai:YOUR_DEPLOYMENT_OR_MODEL_ID",
    temperature=0,
)
typed_model = model.with_structured_output(Extraction)
result = typed_model.invoke("Classify this fictional ticket.")
assert isinstance(result, Extraction)
~~~

Provider syntax, with_structured_output support and tool/provider native strategy depend on installed LangChain and integration package. Do not assume every provider supports JSON schema natively. Prompt temperature 0 does not guarantee repeatability or ground truth.

## Production issue: tool side effects
Before a model invokes a tool, validate tool argument JSON, allowlisted name, per-tenant permissions and consent; journal idempotency and outcome. Treat retrieved documents and tool result content as untrusted. Unlimited tool loops can exhaust tokens/quotas; cap iterations/time/budget.

## Persistence choices
In-memory agent state is enough for stateless one-shot tasks. For multi-step durable conversations or workflows that must resume after downtime, LangGraph checkpointers persist thread-scoped state; stores can manage cross-thread data. Choose checkpoint durability mode with recovery semantics; never assume "checkpoint exists" means irreversible external side effects are exactly once.

## Testing
Frozen evaluator data for structured outputs, tool action denial and malicious tool-output injection, checkpoint restore after intentional process kill, concurrent sessions and tenant isolation, model migration compatibility, partial streamed tool call. Report exact SDK/provider versions.

Official: https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model and https://docs.langchain.com/oss/python/langchain/structured-output and https://langchain-ai.github.io/langgraph/concepts/durable_execution/ .
