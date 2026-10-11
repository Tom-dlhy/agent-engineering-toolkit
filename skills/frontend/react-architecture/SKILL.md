---
name: react-architecture
domain: frontend
version: "0.1.0"
description: >-
  Use when implementing React component boundaries, hooks, state and performance in a TypeScript frontend. Do not use for Vue, Svelte or non-React applications.
---

# react-architecture

## Components
Keep rendering declarative and separate view-state from business operations. Group components by feature/ownership, co-locate local state and lift only when multiple consumers need it.
## Effects
Effects synchronize with external systems, not routine derived values. Preserve hook rules. Avoid redundant state and effect loops; use memoization only with measured need.
## Data flow
Use framework loaders/server functions when available; avoid duplicate client fetch and server state sources. Validate API results at runtime when needed. Render loading, error, empty, success and optimistic states explicitly.
## Verify
Test interaction behavior and accessibility, not implementation details. Inspect responsiveness, hydration, key stability and real performance traces.
