# LiteLLM gateway failure modes and spend constraints

**Read when:** testing LiteLLM Proxy budgets, virtual keys, fallback,
tenant quotas and combined retry behavior across layers.

## Critical guarantee boundary
Official LiteLLM docs say proxy spend budgets need a backing
PostgreSQL database. A DB-less proxy configured with a budget
can fail open for spend cap. A local YAML value alone is not
a hard ceiling. Team/user/key budget inheritance and routing
precedence are version-sensitive; verify actual installed
LiteLLM and runtime topology.

## Failure matrix
- DB unavailable: decide/test fail-open vs fail-closed
  against approved business budget policy.
- Key scoped to model A: reject nonallowed model and fallback B.
- Region/tenant: cross-provider fallback must honor privacy,
  residency, tools and schema constraints.
- Layered retry: bound total requests across app/router/proxy/
  provider; avoid exponential retry multiplication.
- Price metadata missing: don't represent missing usage as zero
  cost; track reconciliation and reporting limitations.
- Redis/cache interruption: verify virtual-key and quota rules.
- Logging: ensure prompts, tokens, responses and keys don't
  leak into unrestricted proxy logs.
- Model alias and structured-output capability changes:
  rerun provider compatibility evals.

## Validation
Use synthetic tenants, mock upstream and disposable DB first,
then authorized sandbox provider calls. Record exact gateway
revision and whether limits are checked before or after usage
reconciliation; budget reservation might be conservative,
but unpriced output can undermine cost predictions.

Sources: https://docs.litellm.ai/docs/proxy/users ,
https://docs.litellm.ai/docs/proxy/virtual_keys ,
https://docs.litellm.ai/docs/proxy/architecture .
