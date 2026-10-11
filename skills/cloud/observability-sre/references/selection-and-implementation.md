# Cloud observability and SRE — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Start with user-visible success, latency, correctness and freshness SLIs. Separate request availability from CloudWatch/Azure Monitor/Cloud Monitoring collection success; define alert windows and burn-rate policies.

## Implementation decisions
OpenTelemetry propagation is not authentication. High-cardinality tenant IDs/raw paths can blow up metric cost and leak data. Avoid full prompts, secrets and unapproved PII in traces/logs.

## Starter illustration
~~~bash
# Inspect service SLI definition and labels before instrumenting.
# Synthetic outage alert test should run only in isolated staging.
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://sre.google/sre-book/service-level-objectives/
- https://opentelemetry.io/docs/concepts/observability-primer/
