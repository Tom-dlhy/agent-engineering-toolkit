# TanStack Router loaders, Search Params and Query state

**Read when:** the task touches tanstack router loaders, search params and query state, rather than unrelated framework concerns.

## Decision and implementation
**Route contract:** `validateSearch` and route params constrain browser-provided URL input; client code cannot be trusted for business authorization. Route loaders fetch data to render pages, with dependency tracking and invalidation. `beforeLoad` can redirect navigation but cannot protect callable server function.

**Search and cache:** Define typed search filters, location history/back behavior, validate serialization and distinguish loader state from TanStack Query query cache. If using Query integration, avoid calling `fetchQuery` and `useQuery` with mismatched query keys that duplicate requests or show stale identities. Invalidate both relevant cache layers when mutation affects route data.

~~~tsx
// Framework-specific route sketch; exact imports/version must be verified:
export const Route = createFileRoute("/products")({
  validateSearch: (s) => ({ q: typeof s.q === "string" ? s.q : "" }),
  loaderDeps: ({ search }) => ({ q: search.q }),
  loader: ({ deps }) => listPublicProducts({ q: deps.q }),
  component: ProductsPage,
});
~~~
`listPublicProducts` is explicitly a public catalog helper; private queries belong behind server auth checks. Avoid leaking private data into serialized route results.

**QA:** navigate filters/back/forward, invalid query params, abort pending loader, stale response after logout, two tabs, mutation invalidation and SSR hydration with exactly equivalent search state.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://tanstack.com/router/latest/docs/framework/react/guide/data-loading
- https://tanstack.com/router/latest/docs/framework/react/guide/search-params
