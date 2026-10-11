---
name: llm-integration
domain: ai
version: "0.1.0"
description: >-
  Use when developing LLM-backed applications, tool calling, structured outputs, RAG or provider gateway adapters. Do not use for ordinary software with no model involvement.
---

# llm-integration

## Model boundary
Separate business operations from provider-specific SDK responses. Define explicit request/output schemas, timeout, retries, cancellation, concurrency and maximum cost/token limits. Treat model output as untrusted, including tool arguments and retrieved documents.

## Correctness
Validate structured outputs against runtime schemas. Restrict callable tools by allowlist and authorization context; require confirmation for dangerous actions. Build deterministic baseline tests and task-specific evaluations against representative inputs. Instrument latency, retries, error categories, token usage when exposed and fallback behavior.

## Safety and portability
Defend against prompt injection across retrieval, messages and tool descriptions. Keep prompts/templates versioned without secrets. A common adapter can ease switching providers but does not guarantee equivalent models, features or pricing. Avoid hard-coding availability claims without checking documentation.
