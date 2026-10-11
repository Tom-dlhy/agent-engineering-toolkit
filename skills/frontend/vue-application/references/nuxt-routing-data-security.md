# Nuxt 4 loaders, route APIs and authorization

**Read when:** implementing or testing nuxt 4 loaders, route apis and authorization.

## Technical method
1. Determine Nuxt 3 versus 4, actual app/ and server/ conventions, Nitro adapter and server rendering mode. Prefer useFetch/useAsyncData for SSR-aware data transfer; raw $fetch in component setup may refetch after hydration and create waterfalls.

2. Example public usage: const { data, status, error, refresh } = await useFetch('/api/public-products', { query: { page: 1 } }); No authorization follows from calling this composable.

3. Keep secret DB providers in Nitro server/api/ or server utilities. Derive actor from server session, authorize object/tenant on each API request, validate runtime query/body and send safe errors. Route middleware only guards navigation UX, not callable API routes.

4. Nuxt runtimeConfig.public goes to browser and must never hold tokens. When using private SSR caching, ensure key scopes actor/tenant/permissions or avoid shared cache. Test invalid useAsyncData keys, dedupe, canceled navigation, stale data after logout and proxy cookie/origin setup.

5. Version-aware tests: actual Nuxt production build and SSR preview, parallel tenant requests and serialized payload inspection.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://nuxt.com/docs/4.x/getting-started/data-fetching
- https://nuxt.com/docs/4.x/guide/directory-structure/server
