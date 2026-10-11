---
name: modern-python
domain: backend
version: "2.1.0"
description: >-
  Use when engineering Python runtime, packaging, typing, configuration,
  synchronous or asynchronous concurrency and robust command-line or service code.
  Do not replace FastAPI, HTTPX, SQLAlchemy or domain-specific specialists.
---

# Modern Python — production mechanics before abstraction

## Decisions
1. Identify **application type** (script, CLI, package, ASGI API, batch, worker), supported interpreter/runtime and current lock/build conventions. Preserve coherent existing projects.
2. Separate pure calculations from I/O, parse untrusted data at runtime boundaries, enforce type contracts in static checks and handle explicit errors; Python hints do **not** validate inputs automatically.
3. For dependency builds pin tested interpreter and resolved lock. With uv, choose `uv sync --locked` to **check** lock freshness; `--frozen` skips freshness check. Do not treat both as equivalent.
4. Choose concurrency by workload: async for compatible nonblocking I/O; threads for blocking drivers; processes or native releases of GIL for CPU workloads. Never introduce unlimited tasks to hide slow I/O.
5. Own resources at proper lifetime and cancellation boundaries. Do not suppress `CancelledError`, leak file/HTTP connections, or put customer credentials into exceptions or logs.
6. Validate configuration at startup with Pydantic Settings or stdlib as appropriate, including env/dotenv/secret source precedence and unexpected configuration.
7. Prove tests, lint/typing, locks and packaging for **actual deployment platform**, not a solely local REPL success.

## Read only as needed
- [Packaging, uv and reproducibility](references/project-packaging.md) — read when locking, shipping wheels or building containers.
- [Python typing, quality and contracts](references/typing-and-quality.md) — read when designing types, Protocols, exceptions and validation.
- [Async, threads, processes and capacity](references/concurrency-and-performance.md) — read when choosing concurrency or managing cancellation.
- [Settings and injected secrets](references/settings-and-secrets.md) — read when building typed configuration or testing source precedence.
- [CLI and batch reliability](references/cli-batch-and-filesystem.md) — read when building file processing, idempotent batch or command-line automation.
- [Supported runtime and deployment compatibility](references/runtime-lifecycle-and-compatibility.md) — read when changing Python versions, packaging or deploying heterogeneous environments.

## Boundaries
python-project-architecture chooses package/module architecture;
fastapi-service handles HTTP routes/lifespan; background-jobs owns durable queues;
test-strategy owns test-suite design.

## Completion
Runtime and lock pinned; inputs and secrets protected; bounded resources,
correct cancellation/cleanup; appropriate negative tests executed or gaps named.
