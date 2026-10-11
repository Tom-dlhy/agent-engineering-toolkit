---
name: nextjs-application
domain: frontend
version: "0.1.0"
description: >-
  Use when building or modernizing a Next.js app with React server/client boundaries, routing, forms and rendering strategies. Do not use for TanStack Start or Vue projects.
---

# nextjs-application

## Rendering
Choose server versus client components based on actual interactivity and data dependencies. Keep server secrets and privileged operations out of client bundles. Avoid accidental client-boundary expansion and redundant fetching.
## Data
Use framework caching/revalidation deliberately; distinguish static, dynamic and personalized responses. Validate all server actions and enforce authorization on the server rather than assuming hidden buttons are secure.
## Performance
Optimize critical images/fonts, streaming/loading/error states and bundle splitting. Avoid prematurely distributing state across libraries.
## Verification
Run typecheck, build, route tests, critical interaction tests and preview QA. Verify framework-specific behavior against the installed version and official docs.
