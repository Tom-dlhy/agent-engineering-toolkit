# Next.js Server Actions, Route Handlers and security

**Read when:** the task touches next.js server actions, route handlers and security, rather than unrelated framework concerns.

## Decision and implementation
**Endpoint reality:** A Server Action is callable over HTTP; hiding a button or restricting a page layout does not authorize it. Validate `FormData` with a runtime schema, derive actor from authenticated server session, apply object/tenant permission in service/DB and verify CSRF/Origin/cookie assumptions for deployed reverse proxy.

~~~tsx
"use server";
export async function renameOrder(formData: FormData) {
  const id = formData.get("id");
  if (typeof id !== "string" || !/^[a-z0-9-]{1,64}$/.test(id)) {
    throw new Error("Invalid input");
  }
  const actor = await requireActor();  // application-specific
  await renameOrderAuthorized(actor, id, formData.get("name"));
  // Revalidate route/data using API supported by the pinned Next version.
}
~~~
The example intentionally omits `requireActor`/service implementation; actual service must validate name and transaction. Do not echo private error to browser.

**Route handlers:** Use `app/api/.../route.ts` for external HTTP endpoints, webhooks and APIs with separately authenticated identity, signature verification, rate limit, response caching and errors. Server Actions are not general public APIs.

**QA:** direct POST without UI navigation, expired session, forged tenant ID, malformed/form large body, duplicate submit, CSRF, redirect injection, error redaction and error after remote commit. Test built app and staging proxy — not only unit mocks.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://nextjs.org/docs/app/getting-started/updating-data
- https://nextjs.org/docs/app/building-your-application/authentication
