---
name: react-architecture
domain: frontend
version: "0.2.0"
description: >-
  Use when building, reviewing or optimizing framework-agnostic React UI architecture, hooks, state ownership, accessibility, rendering or client data fetching. Do not use for Next.js App Router server actions, TanStack Start server functions, Vue or Svelte-specific runtime APIs.
---

# React architecture — one state owner and explicit rendering boundaries

## Implementation procedure
1. Read React and TypeScript versions, framework, component tree and actual interaction requirements before changing architecture.
2. Choose state by **ownership**: render-time derivation for computed values, component state for local UI, URL/router for shareable navigation, server/query cache for remote state, external global store only for truly shared synchronous UI state.
3. Render must stay pure. `useEffect` synchronizes with an **external system**, not with another local derived value; cancel subscriptions and asynchronous side effects on cleanup.
4. Stable keys correspond to data identity rather than array position when reordering; preserve controlled/uncontrolled inputs, keyboard semantics and focus.
5. Apply `memo`, `useMemo`, `useCallback` only with profiler evidence or a specific supported compiler/use case; avoid render-time mutation and redundant effect loops.
6. Handle loading/error/empty/unauthorized/offline transitions and user-intended optimistic rollbacks.
7. Test realistic interactions, concurrent fetch cancellation, StrictMode development behaviors, accessibility and measured Web Vitals.

## Targeted expertise (open only when needed)
- [state ownership, effect discipline and reusable component contracts](references/react-state-effects-and-boundaries.md) — **read when** state ownership, effect discipline and reusable component contracts.
- [remote data caching, rerenders, concurrency and measured performance](references/react-data-fetching-performance.md) — **read when** remote data caching, rerenders, concurrency and measured performance.
- [interaction-level tests, keyboard navigation and hydration regression](references/react-testing-accessibility.md) — **read when** interaction-level tests, keyboard navigation and hydration regression.

## Boundaries and completion
Choose the one framework-specific skill matching the actual repository. Delegate visual tokens and UI library APIs to design/ui, security audit to quality, endpoint contracts to backend, and deployment infrastructure to Cloud. Do not install frameworks just to follow a skill. Complete with evidence from typecheck/build, negative authorization tests, realistic browser hydration and documented version limitations. Treat examples as illustrative until executed against pinned dependencies.
