# Angular Router, HTTP and authorization

**Read when:** implementing or testing angular router, http and authorization.

## Technical method
1. Router guards can redirect navigation but do not secure backend endpoints; test API directly with expired, guest and other-tenant principals. Lazy loading can reduce bundle footprint, not authorization authority.

2. HttpClient.get<T>() is a compile-time type claim, not runtime JSON validation. Put typed DTO adapters in services, validate untrusted data, distinguish 401/403/429/5xx and provide retry budgets. Use HttpContext or request options to avoid leaking bearer tokens to third parties.

3. Example intent: inject(HttpClient).get<OrderDto>('/api/orders/' + encodeURIComponent(id)); return value still needs runtime checks for sensitive boundaries.

4. Cookie-authenticated APIs require appropriate CSRF strategy and SameSite/Secure cookies. CORS alone does not authenticate calls. Angular HTML sanitation is not license to use bypassSecurityTrustHtml with arbitrary input.

5. Test guard bypass, forged object ID, abort when component destroyed, stale response, malicious redirect, SSR transfer cache exposure and permission removal mid-session.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://angular.dev/guide/routing/route-guards
- https://angular.dev/guide/http
- https://angular.dev/best-practices/security
