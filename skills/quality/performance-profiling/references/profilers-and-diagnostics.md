# Profilers and diagnostics — isolate the expensive operation

**Read when:** CPU, memory, async waiting, database calls or browser rendering
affect measured latency or throughput.

| Symptom | Inspect first | Limitations |
|---|---|---|
| CPU-bound Python | cProfile/pstats or sampled py-spy | Observer overhead; sampling variance |
| Python allocations | tracemalloc snapshots + process RSS | Native allocations may be invisible |
| Low CPU, high API p99 | OTel spans, pool/queue waits | Network or provider latency |
| DB query latency | query counts, EXPLAIN, locks/transaction | More workers can worsen pool pressure |
| Frontend interaction | browser trace, INP, LCP, CLS | Desktop lab != real mobile field data |

### Reproducible Python profiler example

~~~bash
python -m cProfile -o /tmp/app.prof -m app.benchmark
python -c 'import pstats; pstats.Stats("/tmp/app.prof").sort_stats("cumtime").print_stats(25)'
~~~

Run only if the local project's benchmark module is available, controlled
and authorized. Compare cumulative time, per-call cost and call counts;
profile overhead changes timing. py-spy attaching to running processes
can require privileged tracing; do not attach to other users' production
workloads without permission.

## Async and resource bottlenecks

A "fast CPU" report may still have network queues, database locks or
connection-pool wait. Separate queue/admission, DNS/connect, read, DB lock,
serialization and external model inference in spans. Multiple ASGI workers
multiply open pools and resident memory, so optimizing concurrency requires
downstream capacity calculations too.

## Evidence

Specify environment, runtime, input data, concurrency, warmup, profile
tool/version, metric unit and unexplained instrument overhead. Prefer
the bottleneck actually affecting a user SLO over the hottest isolated
microbenchmark. Never log raw PII, prompt inputs or security headers
for performance profiling.

Official: https://docs.python.org/3/library/profile.html ,
https://docs.python.org/3/library/tracemalloc.html ,
https://opentelemetry.io/docs/languages/python/instrumentation/ .
