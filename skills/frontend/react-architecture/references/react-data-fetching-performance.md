# React async resources, mutation UX and performance

**Read when:** the task touches react async resources, mutation ux and performance, rather than unrelated framework concerns.

## Decision and implementation
**Avoid fetch waterfalls:** Prefer router/framework loader for critical data. In client-only code, use a server-state cache when stale/refresh/retry/pagination/synchronization complexity justifies it; avoid duplicated `fetch` effects in sibling components. A TanStack Query cache is not a replacement for authorization on server APIs.

**Cancellation/ordering:** Rapid filter changes can make old request finish last. Pass an AbortSignal where supported, and ensure only the current key updates the visible state. A mutation with optimistic data must rollback on failure and invalidate authoritative cache after success.

**Measure first:** Inspect React DevTools Profiler and browser long tasks, JS bundle, INP and React commit latency. Splitting expensive code using lazy/Suspense might improve initial JS but can create loading waterfalls. `memo` stops some renders only when props comparison permits; React Compiler availability/version is a project-specific decision.

**Anti-pattern:** `const data = await fetch(...)` inside a browser component render without framework resource semantics; uncontrolled infinite retry; `useMemo` everywhere without observed gain; parsing MB JSON synchronously on interaction.

**Tests:** Simulate fetch racing, 429, aborted navigation, cache invalidation, optimistic failure, offline and 5x latency. Profile large list, avoid assuming 1000 items implies virtualization is always warranted.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://react.dev/learn/you-might-not-need-an-effect
- https://tanstack.com/query/latest/docs/framework/react/overview
