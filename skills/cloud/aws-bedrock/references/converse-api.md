# Bedrock Converse API integration (Python)

**Read when:** calling Bedrock-runtime `converse`, composing messages, parsing output, or handling model compatibility.

## Preconditions

Install a reviewed boto3/botocore version; identify `region_name`, account permissions, an enabled model or inference profile ID and relevant token limits. The IAM policy must grant the action(s) needed for the chosen runtime operations on permitted model/profile resources. Not every model supports every inference parameter, tool type or modality. Consult the exact model compatibility table.

## Minimal text conversation

```python
import boto3
from botocore.config import Config

client = boto3.client("bedrock-runtime", region_name="eu-west-3", config=Config(
    connect_timeout=3, read_timeout=60,
    retries={"mode": "standard", "max_attempts": 2}
))

def generate_answer(model_id: str, question: str) -> str:
    response = client.converse(
        modelId=model_id,
        messages=[{
            "role": "user",
            "content": [{"text": question}],
        }],
        inferenceConfig={"maxTokens": 400, "temperature": 0.2},
    )
    stop_reason = response.get("stopReason")
    if stop_reason not in ("end_turn", "stop_sequence"):
        raise RuntimeError(f"generation did not finish normally: {stop_reason}")
    content = response["output"]["message"]["content"]
    texts = [block["text"] for block in content if "text" in block]
    if not texts:
        raise RuntimeError("no text content block in model response")
    return "".join(texts)
```

Use an **allowed and compatible** `model_id`; this example does not discover the current model catalog or guarantee availability. Not every valid response ends in text: tool use, guardrail blocking and other content types require branching rather than concatenation.

## Response handling

- `output.message.content` is a list of tagged-union content blocks; check each block type rather than assuming `text` at index 0.
- `stopReason="tool_use"` means the caller must inspect `toolUse`, authorize/execute an allowlisted function and send a matching `toolResult`. The model does not execute tools on its own.
- `usage` can contain input/output token counts if supported; record aggregate statistics without storing confidential prompts.
- Handle model quota/throttling, validation errors, access denial, request too large and network timeouts separately.
- For RAG, treat retrieved documents as data, not higher-priority instructions.
- For structured output, validate actual response with JSON schema/Pydantic after generation; schema instructions alone are not a runtime guarantee.

## Testing

Fake Bedrock client: normal answer, empty blocks, tool_use stop, guardrail stop, max_tokens stop, throttle, invalid JSON, access denied. Sandbox tests with the permitted model/region; log latency and usage without raw sensitive content.

Official: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html and https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html .
