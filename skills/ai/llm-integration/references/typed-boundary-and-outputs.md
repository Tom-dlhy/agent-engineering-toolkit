# Typed model port and structured output

**Read when:** insulating domain/application logic from an LLM SDK or enforcing structured response contracts.

## Application-owned normalized result

~~~python
from dataclasses import dataclass
from typing import Protocol
from pydantic import BaseModel

class Classification(BaseModel):
    category: str
    confidence: float  # add Field(ge=0, le=1) in real contract

@dataclass(frozen=True)
class GenerationResult:
    text: str
    provider: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None

class TextGenerator(Protocol):
    async def generate(self, *, prompt: str) -> GenerationResult: ...
~~~

This normalized contract is illustrative for **text-only** results. Model tool requests, multimodal parts, safety blocks, streaming deltas and usage provenance require separate explicit variants. Don't silently discard content blocks or assume all providers expose identical token counts.

## Validation boundary

Use provider-native structured output if supported by the exact model; otherwise guarded JSON/tool strategy and Pydantic validation. A prompt instruction "return JSON" is not validation. Handle truncated/empty output and schema changes as typed errors; only apply bounded repair when safe and evaluated, never assume retry magically improves correctness.

~~~python
from pydantic import BaseModel, Field, ConfigDict

class CategoryAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str = Field(min_length=1, max_length=60)
    explanation: str = Field(max_length=500)
~~~

For business-critical values, constrain with Enum, regex, model validators and downstream authorization. Model-provided confidence is not calibrated probability unless calibrated against a labeled dataset. A validated tool argument isn't authorization.

## Provider adapter ownership

Bedrock Converse returns content block unions, stopReason/toolUse and usage. Google Gen AI returns candidates/parts and finish reason/safety metadata. Azure/OpenAI Responses returns typed output items. An adapter should preserve information required to decide if output is final or a tool call, not flatten every result to text.

## Streaming

Define delta protocol, final completion event, error event and disconnect/cancellation semantics. Never call model output final on first chunk, and do not commit business side effects from partially validated JSON.

## Review
Test missing text block, refusal, max-token stop, invalid schema, ambiguous tool request, quota and incomplete stream. Store prompts/version identifiers rather than raw personal text in shared traces.

Official: https://docs.pydantic.dev/latest/concepts/models/ and https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html and https://docs.langchain.com/oss/python/langchain/structured-output .
