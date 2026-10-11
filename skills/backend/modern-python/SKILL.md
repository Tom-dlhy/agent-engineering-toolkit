---
name: modern-python
domain: backend
version: "0.1.0"
description: >-
  Use when structuring Python projects with type hints, uv, packaging, testing, linting and robust runtime behavior. Do not use when Python is not the implementation language.
---

# modern-python

## Project conventions
Specify supported Python versions, use `pyproject.toml` with a reproducible dependency lock, source layout appropriate to distribution needs and narrow public interfaces. Use `uv` when compatible with project conventions.
## Correctness
Use type hints and static checking for boundaries, explicit exceptions, context managers for resources and dataclasses or Pydantic only when appropriate. Avoid shared mutable defaults, hidden globals, import-time side effects and broad `except Exception` handlers.
## Testing
Use pytest/unittest with temp directories and deterministic fixtures. Unit-test pure logic; integration-test database, filesystem and HTTP boundaries. Run `ruff`, type checker, tests and packaging smoke checks per project's documented toolchain.
## Performance
Profile before async or concurrency rewrites; distinguish I/O-bound from CPU-bound work.
