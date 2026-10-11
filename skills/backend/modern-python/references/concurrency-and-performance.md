# Concurrency, throughput and scaling with Python

**Read when:** selecting sync/async/thread/process/queue or investigating user-load, latency and capacity.

## Decide from the bottleneck

| Workload | Default strategy | Failure mode |
|---|---|---|
| Small synchronous work | Normal function | Overengineering async |
| Many independent network calls | asyncio + truly async SDK | Pool exhaustion/429/unbounded tasks |
| Blocking SDK in async app | Sync handler, worker thread or async alternative | Blocking event loop |
| CPU-heavy Python | Native/vectorized implementation or process workers | GIL, IPC serialization, memory |
| Durable long-running work | Broker/worker, job state, DLQ | Duplicates and unbounded backlog |
| Hosted model calls | Bounded async requests if supported | Provider token quotas, long p99 |

~~~python
import asyncio

async def fetch_bounded(ids: list[str], fetch):
    sem = asyncio.Semaphore(8)
    async def one(item: str):
        async with sem:
            return await fetch(item)
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(one(i)) for i in ids]
    return [t.result() for t in tasks]
~~~

8 is illustrative; choose concurrency based on outbound pool, provider RPM/TPM, memory, tail latency and business deadline. Creating 100k awaiting tasks still consumes memory: batch or use bounded queues.

## Scale is not a user count
Use request arrival rate, concurrency, average and p95/99 durations, I/O fanout, bytes held, DB connection budgets, CPU and SLO. Little's Law (L = λW under stable conditions) helps reason about in-flight work, not establish universal thresholds for 100/1,000/100,000 users.

Each additional ASGI worker multiplies connection pools and process memory; upstream DB and LLM quotas may bottleneck before CPU. Retries under 429 can amplify congestion; apply backpressure, capped attempts, deadlines, cancellation and appropriate queueing.

## Verify
Load realistic bursts, measure completed requests not just offered traffic; inspect CPU, RSS, event loop lag, open connections, pool wait, p99 latency, provider 429, queue age and recoverability. Prefer profiling to ungrounded refactors.

Official: https://docs.python.org/3/library/asyncio-task.html and https://docs.python.org/3/library/concurrent.futures.html and https://www.python-httpx.org/advanced/resource-limits/ .
