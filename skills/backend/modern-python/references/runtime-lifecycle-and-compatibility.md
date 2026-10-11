# Python runtime compatibility, uv locks and deployment images

**Read when:** upgrading interpreter, dependencies, container/runtime
architecture or distributing Python library/CLI/API to production.

## Lock and sync are different operations

~~~bash
uv lock --check
uv sync --locked --no-dev
uv run --locked python -m unittest discover -s tests
~~~

Official uv docs: --locked checks if current project manifests
still agree with uv.lock, and fails rather than updating the
lock. --frozen uses the existing lock without freshness check.
Do not call frozen and locked equivalent. An immutable lock
is useful reproducibility evidence, not malware-free proof.

## Platform compatibility

Python version and dependency constraint alone cannot establish
that required CPython/ABI wheels exist for Linux musl/glibc,
Windows or macOS. Verify native dependencies, SSL library,
image CPU architecture, optional extras and actual import/build.
An upgrade can change interpreter performance, extension behavior
and event-loop/async runtime; re-run integration suite.

## Container release
Pin trusted base image digest, make final image non-root,
separate build secrets from runtime, install exact lock,
enforce health/readiness and graceful SIGTERM. Official uv
Docker guide distinguishes intermediate workspace stages
where only some manifests are copied, and discusses
non-editable installs for release images. Don't blindly
paste versionless Docker tags into production configs.

## Lifecycle/capacity tests

Missing required environment variable must fail at startup,
shared clients must close, connections must not multiply
unexpectedly with workers, fork/process isolation must be
reviewed, and readiness must reflect needed dependencies
rather than always returning 200. Measure RSS/CPU and
worker shutdown on target runtime, not inferred user counts.

Sources: https://docs.astral.sh/uv/concepts/projects/sync/ ,
https://docs.astral.sh/uv/guides/integration/docker/ and
https://docs.python.org/3/library/venv.html .
