# Project packaging, uv and reproducibility

**Read when:** scaffolding a package/service/CLI, modifying pyproject, or planning a reproducible Python deployment.

## Pick a layout by artifact
| Artifact | Minimum | When to evolve |
|---|---|---|
| One-off exploration | Script, documented env, input contract | Becomes repeated service or shared library |
| Installable library/CLI | pyproject, package (often src), tests, entrypoint | Stable public API and publishing |
| API/worker service | App package, runtime entrypoint, lock, Docker/tests | Independent bounded contexts |
| Notebook/research | Notebook + reproducible Python functions | Production logic moves to tested modules |

`src/` layout can prevent accidental imports from working checkout; flat layout is valid for application-only code. Do not force DDD on trivial services.

~~~toml
[project]
name = "example-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "httpx>=0.27", "pydantic>=2"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
~~~

The version ranges are illustrative; resolve/pin a tested lock for the target runtime instead of blindly accepting old lower bounds. Keep .env, tokens, wheels and .venv out of git.

~~~bash
uv sync --locked
uv run --locked ruff check .
uv run --locked pytest -q
uv run --locked mypy src
uv build
~~~

`uv run --locked` validates lock freshness; `--frozen` trusts a lock without freshness checks. A CI that automatically regenerates the lock obscures dependency drift. Include import/package smoke test from outside the repo when distributing. Deploy with a non-root image, graceful termination, config fail-fast and pinned verified Python/base image.

## Verification
Compatible Python runtimes, lockfile reproducibility, unit/integration/build tests, dependency and license review, no runtime import from local checkout, negative missing-dependency test.

Official docs: https://docs.astral.sh/uv/concepts/projects/sync/ and https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ .
