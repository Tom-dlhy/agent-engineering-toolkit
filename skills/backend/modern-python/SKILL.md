---
name: modern-python
domain: backend
version: "2.0.0"
description: >-
  Use for Python runtime, package structure, type safety, dependency management, concurrency choices, configuration and Python-specific code quality. Do not use instead of FastAPI, SQLAlchemy, HTTPX or LLM provider specialists.
---

# Modern Python — engineering foundations

## Decide before scaffolding
1. Identify project type (one-off script, CLI/library, worker, API, ML experiment), Python versions, package manager, lockfile, deployment platform and existing conventions. No migration for fashion.
2. Define untrusted inputs, domain invariants, side-effect boundaries, error contracts, lifecycle and cancellation.
3. Choose sync versus async from actual I/O drivers and latency; do not use async as a CPU acceleration technique.
4. Select the lightest project structure that preserves testing and deployment. Record reasons before introducing extra abstraction.
5. Establish reproducible builds, typed boundaries, static checks, deterministic tests and release/rollback criteria.

## Targeted references
- [Python packaging, uv and builds](references/project-packaging.md) — read when choosing project layout, dependency pinning, locking, CI or distribution.
- [Typing, domain contracts and exceptions](references/typing-and-quality.md) — read when defining interfaces, data types, validation or reviewing maintainability.
- [Concurrency, capacity and performance](references/concurrency-and-performance.md) — read when deciding sync vs async, threads/processes/workers, rate limits or bottlenecks.
- [Pydantic settings and secrets](references/settings-and-secrets.md) — read when setting env config, cache lifetime, secret injection and fail-fast startup.

Use python-project-architecture for layout decisions, fastapi-service for ASGI, python-http-clients for outbound REST, python-persistence for databases, python-observability for telemetry, and llm-integration for models.

## Done
Version and toolchain recorded, type/lint/test/build commands run where available, runtime budgets and failure modes examined, no secret or hidden global side effect.
