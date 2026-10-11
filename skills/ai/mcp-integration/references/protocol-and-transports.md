# Model Context Protocol 2026-07-28 core and transports

**Read when:** implementing MCP host, client, stdio/HTTP server,
version migration or tool/resource discovery.

## Current-version fact check
Official 2026-07-28 MCP specification was released (not only a draft).
Core JSON-RPC requests are stateless/self-contained and use
per-request capability negotiation; the previous protocol's
session-oriented assumptions should not be copied. Remote
Streamable HTTP methods/names have routing headers under the
2026 protocol, enabling proxy-based auth/metrics; inspect
actual SDK support. Local stdio is a different process
security and lifecycle surface, not an unauthenticated
HTTP service.

## Features
Tools = callable operations with schema and effects;
resources = data/context accessible with permissions;
prompts = reusable templates. Tasks, Skills over MCP
and MCP Apps are **extensions**; advertise/negotiate
support rather than assuming every client implements them.
Long-running Tasks extension is not the old experimental
2025 core lifecycle.

## Deployment choices
- Stdio: host spawns local executable with restricted
  environment, paths, filesystem and credentials. Avoid
  arbitrary remote packages run with admin privileges.
- Streamable HTTP: TLS, managed identity/OAuth, issuer/
  audience validation, scopes, egress/ingress policy,
  rate limits, remote server lifecycle and retries.
- Client: respect list metadata/caches, tool names and
  schemas, handle partial/error response and cancellations.

## Version proof
Record MCP spec date, SDK major, transport and capability
handshake; test client/server with pinned matrix.
TypeScript SDK v1 line targets 2025-11-25; v2 has
separate server/client packages and supports newer spec.
Do not paste snippets across major versions.

Sources: https://modelcontextprotocol.io/specification/2026-07-28 ,
https://blog.modelcontextprotocol.io/posts/2026-07-28/ ,
https://ts.sdk.modelcontextprotocol.io/ .
