# TanStack Start SSR adapters and deployment QA

**Read when:** the task touches tanstack start ssr adapters and deployment qa, rather than unrelated framework concerns.

## Decision and implementation
**Boundary:** TanStack Start needs compatible runtime/hosting adapter. Inspect server entry, Vite/Rsbuild setup, SSR target and route-manifest build output; adapters and config change across releases. A dev server working on localhost does not establish Cloudflare/Node runtime parity.

**Use server routes intentionally:** Official docs recommend server routes for endpoints called outside a Start application; `createServerFn` is app-internal RPC. Webhooks need HTTP method handling, request body size, auth/signature and idempotency. Never move secrets to client env just to fix dev/preview import issue.

**SSR tests:** Browser test on production preview: full reload deep URL, cached response personalization, initial server/client HTML parity, errors/loading/Suspense, protected navigation, CSRF on direct function calls, CDN headers and route chunk loading. Validate deployment restart and, for persistent service, DB client closing.

**CI:** Typecheck, production build, unit tests for parser/services, Playwright smoke across two browsers, built-client bundle audit for env secrets, verified security headers and adequate Core Web Vitals. Pin framework versions and runner.

**Fault cases:** adapter unsupported API, server context missing during client render, incorrect edge/node SQL driver, origin mismatch behind proxy, broken stream after disconnect, stale asset JS from old build and guest seeing auth data from a cached payload.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://tanstack.com/start/latest/docs/framework/react/guide/server-routes
- https://tanstack.com/start/latest/docs/framework/react/guide/hosting
