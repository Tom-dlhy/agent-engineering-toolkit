---
name: mcp-integration
domain: ai
version: "0.1.0"
description: >-
  Use when implementing Model Context Protocol clients or servers,
  tools/resources/prompts, protocol negotiation, transports,
  OAuth authorization, registries or MCP SDK migrations.
  Do not use for a standalone LLM function call without MCP.
---

# MCP integration — wire protocol, authorization and tool contracts

## Version awareness
The officially released **2026-07-28** MCP specification has a
stateless protocol core and significant changes from 2025-11-25.
Confirm client/server SDK version support before following samples.
Do not mix 2025 session headers/tasks/list semantics into 2026 clients.
The v2 TypeScript SDK uses separated client and server packages; SDK
v1 docs cover an older protocol line.

## Procedure
1. Clarify host/client/server roles and supported protocol/version,
   transport (stdio local vs Streamable HTTP remote), identity,
   deployment and tool/resource/prompt needs.
2. Enumerate tools with stable names, parameter/output schemas,
   side effects and required scopes. Validate arguments server-side
   and run user/tenant authorization **at each call**.
3. Implement auth per spec and deployment: OAuth metadata, issuer,
   audience, scopes and token lifecycle. For local servers, restrict
   install commands/files and isolate processes/credentials.
4. Keep MCP tool descriptions/resources and returned text lower trust.
   Consent and approval policy must be enforced outside the model.
5. Plan transport retries, cancellations, tool result errors,
   cacheable list semantics and server evolution/version negotiation.
6. Test hostile descriptions, changed tool catalog, missing auth,
   cross-tenant invocation, malicious arguments, resource exhaustion
   and partial/failed remote execution.
7. Record migration checklist and interoperability against an
   actually pinned client/server SDK, not specification headings alone.

## References
- [MCP protocol 2026 lifecycle and transport](references/protocol-and-transports.md)
  — **read when** wiring client/server and choosing stable SDK version.
- [Auth, scopes and tool execution trust](references/auth-and-tool-contracts.md)
  — **read when** handling remote credentials, tool actions or approval.
- [Compatibility, registry and adversarial tests](references/migrations-and-interoperability.md)
  — **read when** migrating 2025 clients or testing third-party servers.

## Boundaries
agent-tool-safety defines model-side adversarial policy;
agent-orchestration owns persisted workflows and approvals;
external-skill-audit governs third-party **skill** imports,
which are not equivalent to MCP server integrations.

## Completion
Pinned protocol/SDK, transport and auth interoperability proof,
safe tool contracts and explicit unsupported features or tests.
