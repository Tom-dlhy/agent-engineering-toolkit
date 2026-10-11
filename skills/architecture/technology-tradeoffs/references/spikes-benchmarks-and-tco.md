# Proof-of-concept as a falsifiable technology decision

**Read when:** vendor/framework compatibility, p99, scale
or total cost is an unresolved material risk.

## Build the smallest informative spike

Example: compare one native Bedrock SDK implementation vs
LiteLLM SDK under exactly one authorized account.
Test identical model/region/input with schema output,
tool use, timeout, 429, cost usage, trace and
clean shutdown. Do not automatically include LangChain or
a gateway if it offers no needed functionality.

Define **decision threshold** before measuring:
the abstraction must preserve required tools, meet app SLO
and comply with data residency. Measure p50/p95/p99,
successful useful requests and costs; budget key material
and scrub prompts/logs. A run with only mocked SDKs cannot
prove actual cloud identity and quota behavior.

## Benchmark controls

Record SDK, runtime, OS, hardware, DB size, driver, model
deployment, request size, concurrency, cache and warmup.
Control input distributions and failure injection. Report
sample counts/error rate; do not claim one microbenchmark
shows system-wide production capacity.

## TCO dimensions

Engineering implementation, code migration, infrastructure,
request/token/egress charges, licenses, support/on-call,
security review, observability and recovery. Distinguish
hard vendor prices at research date from approximations.
Service bills at low scale and break-even at high scale
must include idle baselines and operator burden.

## Evidence ledger

| Claim | Proof | Status |
|---|---|---|
| Adapter supports structured JSON | Model integration test | Not run without credentials |
| UI library works with chosen bundler | Build/package smoke | Run in repo |
| DB supports workload | Staging query/load | Needs representative data |
| Cloud is GDPR compliant | Legal/security controls review | Cannot infer from region name |

Don't fill missing measurements with made-up numbers or
quietly treat prototype mocks as production-ready.

Sources:
https://learn.microsoft.com/en-us/azure/architecture/guide/ and
https://sre.google/sre-book/service-level-objectives/ .
