# Adapter contract tests, isolation and boundary pitfalls

**Read when:** writing a DB/HTTP/cloud adapter or validating an existing hexagonal architecture.

## Two complementary tests
- Application fake tests: policy and error behavior, no network, fast deterministic.
- Real adapter contract/integration tests: DB locking/transaction, HTTP status/schema, cloud IAM/region/model capabilities, network timeouts and retry behavior.

Fake matches an application-owned port contract, but doesn't confirm real provider behavior. Version-pin SDK tests and run sandbox calls only when explicitly authorized, especially LLM calls with cost.

## Anti-pattern review
- Infrastructure SDK types in Protocol signature.
- GenericRepository with hundred methods mimicking all ORM operations.
- ORM/Pydantic request object as Domain Entity without explicit reasoning.
- Catching all httpx.HTTPStatusError and converting to UpstreamUnavailable.
- Fake repository that silently supports transactions while real DB doesn't.
- Unit of work with a 60-second model call inside open SQL transaction.
- Mutable global adapter where per-request tenant credentials leak.
- Outbox-free dual writes while declaring "exactly once".

## Selection by project size
Small CRUD can have API + service + concrete adapter, no extra interfaces. A workflow with several providers and side-effect boundaries may justify typed Protocols. A mature modular monolith may enforce package dependencies and adapter-specific contract suites.

## Verification report
Which ports exercised, which real adapters tested, which negative paths failed, what lifecycle/permissions remain unverified. Use runtime tests to confirm imports/DI; folder names alone prove nothing.

Official: https://docs.python.org/3/library/typing.html and https://www.python-httpx.org/advanced/transports/ and https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html .
