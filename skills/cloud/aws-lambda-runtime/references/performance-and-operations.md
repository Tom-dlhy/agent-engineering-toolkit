# Lambda performance, concurrency and deployment

**Read when:** deploying functions, diagnosing timeout/cold start, planning VPC networking, secrets or production resilience.

## Performance decision sequence

1. Measure duration and memory use on representative payloads. CPU allocation increases with memory; benchmark actual cost/latency instead of choosing a tiny memory setting blindly.
2. Inspect cold start vs warm duration, package/import latency, dependencies/layers, initialization and network connection reuse.
3. Set function timeout longer than legitimate work but shorter than upstream/downstream effective budgets. Configure outbound requests with explicit deadlines.
4. Compute maximum concurrent downstream load. Reserved concurrency caps function scale but also limits burst processing; provisioned concurrency can reduce startup latency at additional cost.
5. Watch asynchronous source semantics (SQS batch window/visibility or EventBridge retries), not just Lambda handler errors.

## Packaging

Pin exact package versions and compatible compiled wheels for runtime architecture. Avoid bundling dev dependencies and credentials. Validate handler module/function, environment variable names, zip/container architecture, runtime compatibility and entrypoint. Use immutable deployment versions/aliases when rollback requirements justify them.

## Networking and identity

A VPC-connected Lambda needs correct subnet/security group and route/NAT or private endpoint configuration to reach dependencies. Do not assume attaching a function to a private subnet automatically provides internet access. Execution roles govern AWS API calls; resource policies govern who can invoke. Keep secrets in managed secret stores or protected configuration, with role scope and refresh plan.

## Operational checklist

| Signal | Why it matters |
|---|---|
| Errors, duration p95/p99 | User-visible reliability and latency |
| Throttles, concurrent executions | Capacity mismatch or unintended fan-out |
| Init duration/cold start | Tail latency |
| Async event age / destination failures | Retried or undeliverable async processing |
| SQS oldest message age / DLQ depth | Backlog/poison messages |
| AWS SDK downstream throttling | Retry amplification |

Avoid logging event bodies wholesale. Correlate request ID, sanitized business ID and downstream AWS request IDs. Set alarms that carry an operator action and a runbook.

## Failure drills

Kill worker after external write before recording completion; introduce S3 timeout; exhaust concurrency; deny KMS decrypt; disable upstream dependency; replay same message. Validate idempotency and rollback/replay paths.

Official: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html and https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html .
