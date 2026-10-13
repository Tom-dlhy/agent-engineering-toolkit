# Cloud observability and SRE — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Start with user-visible success, latency, correctness and freshness SLIs. Separate request availability from CloudWatch/Azure Monitor/Cloud Monitoring collection success; define alert windows and burn-rate policies.

### Request-based burn-rate contract
For target good-event fraction `s`, with `0 < s < 1`, define
`burn_w = (bad_events_w / total_events_w) / (1 - s)`.
Use the **same eligible event population** in numerator and denominator.
The period's request-based error budget is
`eligible_period_events * (1 - s)`. Inferring a consumed *period* budget
from a smaller time window requires an explicit traffic assumption.

For a selected multi-window alert, document the long/short windows and
the justified burn threshold. **Page only when BOTH windows breach**:
a recovered short window no longer meets this paging condition. Do not
set universal thresholds or apply this request-based formula automatically
to time-based/freshness SLOs.

Illustration, not a default: `s = 0.999` and 50 bad events among 10,000
eligible events gives a burn rate of 5. With an illustrative threshold
of 4, long=5 and short=6 triggers the page condition; long=5 and
short=2 does not.

Missing telemetry or a zero denominator is UNKNOWN, **not** success.
Route telemetry loss separately from user-impact alerts: an exporter
outage does not prove user requests failed. Low traffic requires a
deliberate signal policy.

Test both windows breaching, recovered short window, missing metrics,
zero traffic and target fractions outside `0 < s < 1` before authorized
staging fault injection.

Source reviewed 2026-10-13: https://sre.google/workbook/alerting-on-slos/

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
