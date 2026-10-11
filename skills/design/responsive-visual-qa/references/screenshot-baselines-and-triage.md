# Screenshot baselines, determinism and defect triage

Read when: creating or reviewing visual regression snapshots, unstable screenshot tests, or deciding whether a diff is real.

## Stable capture contract
Record actual browser engine/version, OS/font packages, DPR, viewport CSS pixels, locale/time zone, color scheme, route and test data. Fix random fixture IDs, dates, animations and network races. Wait for required fonts and intended content; don't mask a data-loading defect by sleeping a guessed amount. Mask only explicitly non-deterministic data (e.g. known third-party dynamic avatar) while still asserting that it exists semantically.

Example Playwright idea (adapt to installed version and runner; do not assume package installed):
```ts
await page.setViewportSize({ width: 390, height: 844 });
await page.goto('/checkout');
await expect(page.getByRole('heading', { name: 'Checkout' })).toBeVisible();
await expect(page).toHaveScreenshot('checkout-mobile.png');
```
A snapshot is not an accessibility audit and a screenshot suite cannot prove interaction correctness. Pair captures with keyboard focus, click/submit and error-state behavior assertions.

## Review diffs like a defect
1. Triage: expected deliberate change, actual regression, flaky animation/time, environmental rendering difference, or unapproved asset/content drift.
2. Inspect before/after at same state and context. Identify affected region, loss of information, alignment or hierarchy.
3. Repair the component/token root cause; recapture selectively.
4. Update baseline only with a reason and review evidence. Never rubber-stamp wholesale snapshots just because a major redesign occurred.

## Guardrails
Screenshots may contain PII: use synthetic data and restrict artifact retention. Do not claim device testing from an emulated viewport. If animation masking is used, still separately test reduced motion and open/close end states.

Official: https://playwright.dev/docs/test-snapshots and https://www.w3.org/WAI/WCAG22/Understanding/reflow
