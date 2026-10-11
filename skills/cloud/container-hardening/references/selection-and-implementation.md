# OCI/Docker image and runtime hardening — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Use supported base image pinned digest, multi-stage build, deterministic lock, non-root user, no secrets baked into layers, explicit health/stop signals and needed capabilities only.

## Implementation decisions
Docker build secrets via BuildKit secret mounts, not ARG/ENV; bind ports and read-only filesystem where workload permits. SBOM/provenance/scans are evidence but not a guarantee of zero vulnerabilities.

## Starter illustration
~~~bash
docker buildx build --check .
# Use RUN --mount=type=secret for build-time secret; no ARG containing credentials.
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://docs.docker.com/build/building/secrets/
- https://docs.docker.com/build/building/multi-stage/
