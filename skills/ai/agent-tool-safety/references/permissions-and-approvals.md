# Agent permissions, approval binding and external effects

**Read when:** model can call payment, file write, cloud deploy,
email, delete, external HTTP, shell, data export or privileged tool.

## Tool call decision
1. Parse tool name against configured registry (not model-defined names).
2. Validate typed args, request size, URL and target tenant.
3. Authorize authenticated actor/action/object on *server* with
   least privilege, not natural-language model assertion.
4. For sensitive effect, persist proposed operation and seek human
   approval bound to normalized exact args/actor/expiry/version.
5. On approval verify current actor, argument digest and resource
   version again; if changed, require fresh approval.
6. Execute with stable idempotency key and bounded timeout.
7. Persist outcome, handle unknown remote commits through reconciliation.

~~~text
propose("delete_report", tenant=T, report=R, operation=K)
  -> validate policy -> AWAITING_APPROVAL
approval(actor=A, operation=K, hash=H, expires=...) persisted
  -> reauthorize A/T/R and check H
  -> execute idempotently -> COMMITTED | UNKNOWN | FAILED
~~~

A checkpoint between approval and call isn't a transaction spanning
the external API. Use provider-supported idempotency or explicit
reconciliation to avoid duplicate money/cloud side effects.

## Security traps
Never use correlation ID or LLM's role tag as auth identity.
A bot owning a privileged service token must not let any tenant
invoke actions outside its own authority. For code execution isolate
FS/network/process/container and limit secrets and egress; human
approval doesn't make malicious tool input harmless.

## Tests
Same approval with changed arguments, expired approval,
cross-tenant actor, replay after worker death, provider
timeout after commit, denied tool chosen by model,
approval cancellation and audit record redaction.

Sources: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ ,
https://modelcontextprotocol.io/specification/2026-07-28 .
