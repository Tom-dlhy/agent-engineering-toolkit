# Cross-layer contracts: frontend, auth, data, runtime and deployment

Read when: matching technologies at their interfaces, especially serverless/edge, SSR, connection drivers and authentication.

## Follow one user request end-to-end
~~~text
browser + assets
  -> public SSR/SSG/hydration and framework router
  -> authenticated server handler (not just client route guard)
  -> validation + per-object/tenant authorization
  -> database driver + connection pool + transaction
  -> storage or queue, if business flow actually requires it
  -> trace/error reporting + recovery + deployment
~~~
This is a **conceptual dependency chain**, not a prescribed monolith. If any link cannot run on the selected platform, the assembled stack is invalid even if each component is popular.

## Compatibility probes
| Seam | Question | Falsifying test |
|---|---|---|
| Framework → deployment | Does target runtime support Node APIs, crypto, streaming, filesystem, SSR adapter and build output? | Pin versions; production adapter build and request smoke |
| Server → database | Is driver HTTP/serverless compatible or raw TCP? Which pool/migration URL? | Deploy minimal authorized read + transaction and rollback |
| Auth → browser/server | Cookie domain/samesite/secure, refresh/revocation, SSR trust, CSRF, bypass via direct RPC/API? | Expired cookie and forged tenant request fail on server |
| ORM → DB | Does dialect/extension/migration provider support requested constraints? | Tiny migration + rollback + representative query |
| Storage → app | Durable object policy, signed URL expiry, permissions, quotas and file size? | Unauthorized read/write rejected |
| Queue → business state | At-least-once retries, dedupe and poison handling? | Duplicate event does not duplicate irreversible action |
| CI → prod | Reproducible builds, provider secrets and required runners? | Run locked build in preview with no production credentials |

Avoid presuming that a framework's documentation example demonstrates cross-cloud adapter portability. Serverless and edge platform limits, connection APIs, release versions and quotas change; check the deployed runtime version and official adapter documentation.

## Architectural ownership
This reference identifies *interfaces that must work*. Exact framework implementation belongs to skills/frontend, DB semantics to database-selection, cloud deployment to cloud and auth adapter/session correctness to authentication-solution-selection + security. Don't hand-roll SDK polyfills merely to fit an arbitrary preferred platform.

Sources: https://docs.cloud.google.com/architecture/framework and https://docs.aws.amazon.com/wellarchitected/latest/framework/perf_architecture_evaluate_trade_offs.html and https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
