# Integration, consumer contracts and browser end-to-end tests

**Read when:** behavior crosses HTTP/DB/message boundaries or user navigation
and must be tested with realistic interfaces rather than internal mocks.

## Integration matrix

| Boundary | Preferred test | Failure scenarios |
|---|---|---|
| Database | Disposable DB matching target dialect, schema migrations | Constraint violation, rollback, concurrent update |
| HTTP client | MockTransport for local error mapping; sandbox separately | Connect/read timeout, invalid payload, 404/429/5xx |
| Broker/worker | Disposable broker + idempotent consumer | Duplicate/redelivery, expired lease, crash before ACK |
| API provider/consumer | Versioned schema/contract with examples | Required field removed, enum addition, response shape |
| Browser | Playwright test of user-visible DOM/accessibility | Auth denied, form error, loading, mobile layout |

Testcontainers can provide ephemeral databases/brokers where Docker and
image access are available and authorized. Pin image versions and isolate
data; live cloud credentials are **not** a routine unit-test dependency.
A Pact-style contract asserts verified agreement for supported interactions
only: it does not certify the provider's entire API or operational behavior.

## Playwright test design

~~~ts
import { test, expect } from '@playwright/test';

test('form displays actionable validation feedback', async ({ page }) => {
  await page.goto('/signup');
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.getByRole('alert')).toContainText('required');
});
~~~

Illustrative fixture: route, accessible names and expected error text must
match the **actual** target application. Prefer role/label locators, assertions
with Playwright's auto-retry, isolation of user sessions and no fixed sleeps.
A DOM assertion is not a substitute for keyboard or manual screen reader QA.
Avoid over-mocking backend network so the single important E2E journey loses
its integration value.

## Producer/consumer evolution

For API changes, verify response shape, status classes, optionality, pagination
and auth, not only 200. A generated OpenAPI JSON file establishes a declared
schema, not wire-compatibility. Preserve backward/forward compatibility
through additive fields and compatible enum behavior where consumers permit;
use versioning when breaking semantics are required.

For messages: use an explicit schema version, idempotency identifier and
consumer behavior on unknown fields/old versions. Test replay after schema
upgrade. Kafka/SQS exactly-once marketing does not make arbitrary downstream
external effects exactly once.

## Isolation and anti-flake

Each test owns fixtures/tenant and cleans its side effects. Use retry in
product behavior where warranted, not test reruns to hide a race. Capture
reproducible seed, clock and schedule; quarantine flakes explicitly with
a maintainer and expiry if necessary, never silently ignore them.

## Security and cost

Do not run E2E against production customers without authority; use synthetic
data and disposable credentials. Database fixtures must not drop arbitrary
configured databases. Integration tests must be clearly tagged and able to
fail fast when needed dependencies are absent.

Official: https://playwright.dev/docs/best-practices and
https://playwright.dev/docs/test-assertions and
https://docs.pytest.org/en/stable/how-to/fixtures.html .
