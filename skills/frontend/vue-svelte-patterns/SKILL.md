---
name: vue-svelte-patterns
domain: frontend
version: "0.1.0"
description: >-
  Use when architecting Vue or Svelte apps with reactive state, typed components and routing, or comparing their component patterns to React. Do not translate React idioms blindly.
---

# vue-svelte-patterns

## Reactive ownership
Keep state colocated with its consumers. Use the framework's idiomatic reactivity, computed/derived values and lifecycle primitives; avoid effects that merely mirror existing state.
## Component contracts
Create typed inputs/outputs, avoid unnecessary global stores and isolate browser-only code when rendering on the server. Respect accessibility and predictable keyboard behavior.
## Routing and data
Use Nuxt/SvelteKit loaders and server endpoints according to the active framework version. Validate server-side authority and route data; handle loading and error cases.
## Verify
Run framework typecheck/lint, build, interaction tests and hydration QA on representative routes and devices.
