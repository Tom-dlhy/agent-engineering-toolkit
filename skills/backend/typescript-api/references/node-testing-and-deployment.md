# Node TypeScript API tests, runtime/toolchain and capacity

**Read when:** implementing Node backend CI, contract and integration
tests, release image or throughput verification.

## Multi-level checks

1. Run strict TypeScript typecheck with pinned tsc and module config.
2. Validate business functions and unknown input with node:test.
3. Test server public HTTP route 2xx, 401/403, 404, conflict,
   malformed JSON/schema and safe 500.
4. Test DB/service integrations against actual disposable dialect;
   fake DB doesn't prove transactional isolation.
5. Verify health/readiness, shutdown under SIGTERM, no leaked handles.
6. Measure p95/p99/error and bounded concurrency with representative
   payloads and downstream quotas when scaling matters.

## Native Node test (illustrative)

~~~typescript
import test from "node:test";
import assert from "node:assert/strict";

function normalize(s: string): string {
  return s.trim().toLowerCase();
}
test("normalizes input", () => {
  assert.equal(normalize("  A "), "a");
});
~~~

Modern Node can strip erasable TS types in supported versions,
but **running a .ts file is not static typechecking**. Pin
Node version, separately run tsc, avoid syntax requiring
transforms under strip-only loader and smoke compiled output.
Do not assume every CI runner's default Node can execute TS.

## Operational and supply-chain boundaries

Verify immutable lock/resolved graph and npm scripts, run tests
on unprivileged CI for untrusted PRs, grant cloud tokens only
to trusted deployment jobs. Validate memory/CPU and event loop
under sustained workload; inspect DB and external API quota,
rather than inventing replica count from user count.

## Evidence
Report actual Node/TS/compiler versions, command, cases,
release artifact revision and known untested integrations.
A passing native test is evidence about its assertions only.

Official: https://nodejs.org/api/test.html ,
https://nodejs.org/api/typescript.html ,
https://www.typescriptlang.org/tsconfig/strict.html ,
https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication .
