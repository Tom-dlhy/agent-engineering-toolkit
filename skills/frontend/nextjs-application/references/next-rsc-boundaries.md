# Next.js RSC boundary, serialization and request authority

**Read when:** the task touches next.js rsc boundary, serialization and request authority, rather than unrelated framework concerns.

## Decision and implementation
**Architecture:** In App Router, page/layout components are Server Components by default. Use `'use client'` at an entrypoint needing state, event handler, browser API, or client hook. All imports from that boundary may enter the client graph; keep server-only DB/auth modules unreachable and consider `server-only` build guard.

**Data flow:** Server Component can call server services without extra internal HTTP fetch. Pass minimal serializable props to Client Component, not ORM credentials, secrets, or raw tenant data. React Server Components can run at build time for pre-render, so a 'server' computation isn't necessarily per-user/per-request.

~~~tsx
// app/orders/page.tsx — server page; reauthorize in service
import { listOrdersForCurrentUser } from "@/server/orders";
import OrderFilter from "./OrderFilter";
export default async function OrdersPage() {
  const orders = await listOrdersForCurrentUser();
  return <OrderFilter orders={orders.map(({id, title})=>({id,title}))}/>;
}
~~~
`OrderFilter` is explicitly client-bound and may never receive private fields. `'use server'` marks server-callable functions/actions, **not** Server Components. RSC internals used by bundlers have their own compatibility caveats; pin React/Next framework pair.

**QA:** inspect emitted JS for server-only imports, test cross-tenant calls directly, static build versus runtime dynamic rendering, unauthorized result serialization, hydration and error boundary.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://nextjs.org/docs/app/getting-started/server-and-client-components
- https://react.dev/reference/rsc/server-components
