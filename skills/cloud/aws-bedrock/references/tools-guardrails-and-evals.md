# Bedrock tool calling, guardrails and evaluation

**Read when:** exposing function calling to a model, chaining agent actions, enforcing guardrails or validating Bedrock application quality.

## Tool calling contract

1. Define JSON schema for each tool in `toolConfig.tools[].toolSpec.inputSchema.json` with minimal parameters and unambiguous descriptions.
2. Treat tool-use input as untrusted; validate with runtime schema, authenticating user/tenant authorization and tool allowlist.
3. For side effects (delete, email, payment, deployment), confirm user intent, permissions and idempotency, independent of model suggestion.
4. Execute via a controlled adapter with timeout, per-tool concurrency and audit. Supply a `toolResult` block tied to the exact `toolUseId`, then call Converse with conversation history including the assistant tool request and user tool result.
5. Limit tool-call depth and total token/cost budget; stop and report unresolved state when exceeding budgets.

Simplified documented shape (not a substitute for checking the installed SDK and model support):

```python
tools = [{
    "toolSpec": {
        "name": "lookup_order",
        "description": "Return public order status after caller authorization",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
                "additionalProperties": False,
            }
        },
    }
}]
# client.converse(..., toolConfig={"tools": tools})
```

Never let a user-provided string select an arbitrary function name; map model tool names to an explicit allowlist. Never trust a "success" claim from the model without checking the external tool result.

## Guardrail limits

Bedrock `guardrailConfig` can protect selected prompt/response text, but **not all tool schemas/results/arguments are necessarily scanned**. Per AWS documentation, `toolResult`, toolSpec descriptions and model toolUse input may not be evaluated by guardrails as ordinary prompt text. Validate these surfaces separately. Guardrails do not replace IAM, tenant authorization or safe tool design.

## Evaluation set

| Scenario | Assertion |
|---|---|
| Happy path factual extraction | Output validates required schema and content rules |
| Refusal/guardrail stop | User receives safe bounded failure |
| Malicious retrieved page | Tool is not invoked with exfiltration parameters |
| Invalid tool args | Runtime rejects without side effect |
| Duplicate retry | External operation is not repeated |
| Model unavailable in region | Failure is classified; no silent provider change |
| Token budget exhausted | Loop stops with resumable error or escalation |

Pin prompt and model/inference profile configuration in eval records, not secrets. Evaluate quality and cost by task type, stratified on failures/edge cases; check current model documentation before deciding fallbacks.

Official: https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html and https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-converse-api.html .
