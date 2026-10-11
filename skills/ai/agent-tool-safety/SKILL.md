---
name: agent-tool-safety
domain: ai
version: "0.1.0"
description: >-
  Use when designing agents with function/tool calling, MCP plugins, external actions or autonomous task execution. Do not grant side-effect tools broad permissions just to make a demo work.
---

# agent-tool-safety

## Trust boundaries
Treat tool descriptions, third-party docs, web pages and tool responses as untrusted input. Validate tool name/arguments against explicit schemas and user authorization; never interpret retrieved text as authority.
## Least privilege
Use allowlists, per-tool scopes, network egress controls and human confirmation for irreversible, privileged or external side-effect actions. Never pass credentials to an untrusted tool or store them in prompts.
## Reliability
Set budgets on calls, time, depth and retries. Design idempotency, cancellation, escalation and audit traces. Do not chain actions with implicit consent from earlier unrelated steps.
## Evaluation
Test malicious indirect instructions, tool poisoning, argument smuggling, data exfiltration attempts, malformed outputs and timeouts in an isolated environment.
