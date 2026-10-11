# MCP compatibility migration, registry intake and adversarial QA

**Read when:** migrating MCP 2025 clients/servers, installing
third-party servers or validating interoperability across SDKs.

## Old vs current
2025-11-25 included experimental Tasks core/session
assumptions. 2026-07-28 removes protocol sessions in
the new stateless core, shifts Tasks into an opt-in
extension and evolves tool/resource listing cache
hints and request headers. New clients must negotiate
capabilities; a compatible **specification date**
is distinct from SDK major release, package version
and transport support.

## Third-party MCP server review
Inspect code/immutable release digest, source/licensing,
setup scripts, requested OAuth scopes/credentials,
network destinations, exported tools/resources and
automatic update behavior. Never run unreviewed
installer with personal credentials. Sandbox and
restrict secrets, filesystem, process and egress.
Tool list from server is untrusted data for model.

## Compatibility test matrix
- Pinned 2026 client ↔ pinned 2026 server basic tools/list,
  tools/call, structured output and errors.
- 2025 legacy ↔ gateway adapter only with explicitly
  supported compatibility; no assumed silent downgrade.
- Cache invalidation after tool catalog/permission change,
  deterministic ordering and TTL behavior.
- OAuth invalid issuer/audience, revoked scope, unknown tool,
  hostile description injection and changed arguments.
- Long Tasks extension only if supported on both sides,
  with per-task identity and authorization on status/cancel.
- Web server restarts/HTTP timeouts and stdio server exit.

## Honest output
Record actual spec/SDK/transport tested and known unsupported
features. A green JSON-RPC transport handshake doesn't
prove tool execution security or privacy compliance.

Sources: https://blog.modelcontextprotocol.io/posts/2026-07-28/ ,
https://modelcontextprotocol.io/specification/2026-07-28 ,
https://ts.sdk.modelcontextprotocol.io/ .
