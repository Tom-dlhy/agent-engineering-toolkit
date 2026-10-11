# Frontend server boundary tests (educational Node fixture)

Run Node.js 24+:

~~~bash
node --test examples/frontend-boundaries/tests/*.test.mjs
~~~

This is a **framework-neutral** HTTP/SSR fixture that verifies real
HTTP requests, server-enforced tenant authorization, response escaping,
deterministic initial HTML, direct RPC denial, Origin check and private
cache policy. It does **not** run Next.js, TanStack Start, Vue/Nuxt,
SvelteKit, Angular or Astro.

No actual identity provider, session signing, CSRF token strategy,
database, durable idempotency or reverse proxy is implemented. In
production each framework requires separate integration/Playwright
tests against its pinned adapter and actual deployment.

Official reference foundations:
https://nextjs.org/docs/app/getting-started/server-and-client-components
https://tanstack.com/start/latest/docs/framework/react/guide/server-functions
https://vuejs.org/guide/scaling-up/ssr.html
