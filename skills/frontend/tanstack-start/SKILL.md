---
name: tanstack-start
domain: frontend
version: "0.2.0"
description: >-
  Use when developing TanStack Start React route loaders, server functions, server routes, middleware, authentication, serialization or deployment. Do not use for Next.js Server Actions, external public HTTP APIs when a server function alone is insufficient, or Vue/Svelte projects.
---

# TanStack Start — typed RPC with enforceable server trust

## Implementation procedure
1. Inspect pinned `@tanstack/react-start`, Router/Query and React versions, server adapter and hosting environment; APIs evolve, so verify version-specific imports before editing.
2. Keep `src/routes` for route definitions/loader/wiring, with reusable view components and services outside route modules when project conventions warrant.
3. `createServerFn()` is **same-origin application RPC**; public/cross-origin endpoints belong in server routes, not callable server functions masquerading as public APIs.
4. **Route beforeLoad is not API authorization.** Enforce identity, tenant/object access and runtime Zod/schema validation inside server function middleware or handler on every private read and write.
5. Current docs install CSRF middleware automatically only if `src/start.ts` is absent; when defining your own `createStart`, explicitly include `createCsrfMiddleware({ filter: (ctx) => ctx.handlerType === 'serverFn' })` or a reviewed equivalent.
6. Distinguish loaders and TanStack Query cached server data; define staleness, loader dependencies, mutation invalidation and optimistic rollback explicitly.
7. Validate SSR/streaming, hydration and serialization with the selected deployment adapter; run production build and direct endpoint negative tests, not only click navigation.

## Targeted expertise (open only when needed)
- [createServerFn validation, middleware, cookies, CSRF and direct invocation](references/start-server-functions-auth.md) — **read when** createServerFn validation, middleware, cookies, CSRF and direct invocation.
- [route search params, loaders, TanStack Query and invalidation](references/start-routing-data-and-cache.md) — **read when** route search params, loaders, TanStack Query and invalidation.
- [SSR, adapters, serialization, deployment and E2E failure tests](references/start-deployment-testing.md) — **read when** SSR, adapters, serialization, deployment and E2E failure tests.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
