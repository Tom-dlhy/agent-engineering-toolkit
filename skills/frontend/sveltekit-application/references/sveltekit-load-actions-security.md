# SvelteKit server loads, actions and route security

**Read when:** implementing or testing sveltekit server loads, actions and route security.

## Technical method
1. Universal +page.ts/+layout.ts load may execute on server for SSR and in browser later. +page.server.ts/+layout.server.ts load is server-only, suited to databases and private environment access. Keep session/tenant state in request locals created through hooks.server.ts.

2. Form actions live in +page.server.ts; native HTML POST works without JavaScript. use:enhance adds progressive UX, not permission or input validation. Authorize user and resource before each mutation, validate FormData via a runtime parser and map safe fail(400) or appropriate HTTP error.

3. Example pattern: export const actions: Actions = { default: async ({request,locals}) => { if (!locals.user) error(401); const input = parseForm(await request.formData()); await updateForActor(locals.user,input); return {success:true}; } }; Functions parseForm/updateForActor are app-specific.

4. CSRF/origin and cookie security depend on configured deployment proxy; test direct action calls, session expiry, forged Origin, duplicate submission, cross-tenant access, disabled-JS fallback and upload limits.

5. Never put private credentials in a universal load or serialized response. Confirm adapter and framework version against docs.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://svelte.dev/docs/kit/load
- https://svelte.dev/docs/kit/form-actions
- https://svelte.dev/docs/kit/hooks
