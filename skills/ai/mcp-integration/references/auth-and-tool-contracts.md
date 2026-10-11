# MCP OAuth, scopes, tool authorization and user consent

**Read when:** exposing MCP tools over HTTP, calling remote MCP
servers or deciding what credentials and tool effects are allowed.

## Three identities
Host application owns user session/consent; MCP client
connects to an authorized MCP server; the actual tool
executor must apply object/tenant authorization.
A tool schema is **not** a permission system. Never
forward an unrestricted host credential to a third
party or allow token passthrough for unintended
audience/resource.

## 2026 authentication changes
2026-07-28 authorization hardening requires verification
of OAuth authorization server issuer (iss) to prevent
mix-up attacks; use appropriate RFC 9207 validated
response and resource/audience scopes as documented.
Some older SDKs implement different registration
flows; do not mix DCR-era examples and CIMD
without checking actual chosen server and SDK.

## Tool contracts
Tool catalog metadata and descriptions are lower-trust
unless from a trusted server, and even trusted tool
responses can contain malicious text. Allowlist tools,
validate arguments at server, restrict egress, apply
per-user/scoped permissions and explicit approval for
irreversible effects. Bind approval to exact proposed
tool+args+actor; recheck upon execution.

## Host and server failure cases
Expired token, wrong OAuth issuer/audience, missing
scope, tool removed between list/invoke, tool name
collision, untrusted local install, malicious description,
cross-tenant resource ID, disallowed URL, canceled
execution after remote mutation, grant revoked midrun.

## Testing
Run against authorized local/sandbox MCP server with
synthetic user identities and controlled fake writes.
Verify 401/403 before mutation and token never appears
in prompt, logs or external proxy traces.

Sources: https://modelcontextprotocol.io/specification/2026-07-28 ,
https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization ,
https://www.rfc-editor.org/rfc/rfc9207.html .
