---
name: aws-bedrock
domain: cloud
version: "2.0.0"
description: >-
  Use when building or debugging Amazon Bedrock inference with Converse, model access and inference profiles, tool calling, guardrails, streaming, quotas or Bedrock-specific SDK integration. Do not use for general OpenAI-only usage or a mere prompt-writing task.
---

# aws-bedrock

## Scope

Bedrock runtime and model capabilities vary by model, region, account access and inference profile. Never assume a model accepts every content block, tool feature or guardrail, nor that `InvokeModel` and `Converse` permissions are interchangeable. Verify the actual allowed API in the project.

## Selection and design

1. Identify application goal, model ID/inference profile, region, account, input modality, latency, tool support and permitted operations.
2. Choose **Converse** for portable conversation shape where supported; use ConverseStream only if streaming is required and supported; never silently replace it with `InvokeModel` when permissions forbid it.
3. Define a strict schema for model responses and tools. Treat model output, tool call arguments and retrieved text as untrusted.
4. Set `maxTokens`, cost, timeout, retries, concurrency and per-user limits; consider refusal, guardrail intervention, truncation and output validation.
5. Capture experiments/evals on representative tasks, including tool misuse, prompt injection, hallucination and malformed output cases.

## Deep references

- [Converse request/response integration](references/converse-api.md) — open for boto3 implementation, message roles, content blocks, errors and model-aware response handling.
- [Tool use, guardrails and evaluation](references/tools-guardrails-and-evals.md) — open for agent tools, validation, security, model evaluations and production controls.

For generic provider interfaces use `llm-integration`; for AWS permission troubleshooting use `aws-iam-security` without loading unrelated services.

## Done

Allowed Bedrock operation confirmed in target account/region; model supported; schema and refusals handled; tool side effects authorized; safety boundaries and trace privacy validated; retries/cost limits explicit.
