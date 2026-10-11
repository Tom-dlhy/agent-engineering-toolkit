# TanStack Start server functions, middleware, input and CSRF

**Read when:** the task touches tanstack start server functions, middleware, input and csrf, rather than unrelated framework concerns.

## Decision and implementation
**Important official semantics:** `createServerFn()` produces a same-origin application RPC endpoint callable directly without loading a protected page. `beforeLoad` guard serves routing UX only; require authorization in function middleware or handler.

~~~tsx
import { createServerFn } from "@tanstack/react-start";
// requireActor and service are application-specific server-only functions.
export const getPrivateOrder = createServerFn()
  .inputValidator((value: unknown) => parseOrderInput(value))
  .handler(async ({ data }) => {
    const actor = await requireActor();
    return await findAuthorizedOrder(actor, data.orderId);
  });
~~~
Check installed version for supported `inputValidator` and middleware chaining; `parseOrderInput` is a runtime parser, not TS assertion. Place server-only imports in server modules and test bundle tree shaking.

**CSRF:** With no `src/start.ts`, Start currently installs its CSRF middleware; custom `createStart` config must add it explicitly:

~~~tsx
import { createStart, createCsrfMiddleware } from "@tanstack/react-start";
const csrf = createCsrfMiddleware({filter: ctx => ctx.handlerType === "serverFn"});
export const startInstance = createStart(() => ({requestMiddleware: [csrf]}));
~~~

CSRF same-origin verification uses Fetch Metadata/Origin/Referer. Do not allow missing Origin headers without a separately reviewed equivalent browser boundary.

**Tests:** direct function call with missing/wrong session, forged input, cross tenant, forbidden external Origin, no origin headers, duplicate mutation, preview reverse proxy origin and accidental public server route.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://tanstack.com/start/latest/docs/framework/react/guide/server-functions
- https://tanstack.com/start/latest/docs/framework/react/guide/middleware
