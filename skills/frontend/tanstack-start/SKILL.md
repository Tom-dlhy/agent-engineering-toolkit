---
name: tanstack-start
domain: frontend
version: "0.1.0"
description: >-
  Use when building a TanStack Start app with server functions, routes, loaders, validation and typed client/server boundaries. Do not use for unrelated frameworks or assume unstable APIs without checking the installed version.
---

# tanstack-start

## Architecture
Keep routes thin: route config, loaders and server function integration; place reusable UI in components, use cases in services and persistence adapters in infrastructure. Validate server-function inputs before executing privileged logic.
## Security
Never trust client-side types for authorization. Enforce permissions inside every sensitive server function. Keep secrets server-only and avoid importing server modules into browser bundles.
## UX and performance
Choose server rendering/caching deliberately; handle pending/error states, invalidation and accessible navigation. Inspect bundle size, hydration and route boundaries.
## Verify
Run app typecheck/build, server-function integration tests, router/navigation smoke tests and deployed preview QA. Confirm TanStack Start APIs from installed version and official documentation.
