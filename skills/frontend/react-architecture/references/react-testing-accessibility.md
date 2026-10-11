# React interaction, accessibility and SSR/hydration QA

**Read when:** the task touches react interaction, accessibility and ssr/hydration qa, rather than unrelated framework concerns.

## Decision and implementation
**Behavior contract:** Test the app from user-visible roles and labels, not private hook state. Testing Library favors role/name queries and user events. Verify keyboard activation, focus return from modal, visible error/empty/loading states, radio/checkbox semantics and `aria-live` announcements where needed. Visual snapshots alone cannot prove behavior.

**SSR hydration:** Server HTML must agree with initial client render. `Date.now()`, `Math.random()`, client timezone, `window`, localStorage and invalid tag nesting in render can mismatch. Use deterministic server-provided data then update browser-only details after mount; do not blindly suppressHydrationWarning over structural mismatch.

**Test pyramid:** pure reducers/validation; React component integration with Testing Library; real Playwright Chromium/WebKit/Firefox for SSR, keyboard, responsive and navigation, plus production build preview. On both dark/light themes inspect contrast and reduced-motion.

**Example testing intent (illustrative):**
~~~tsx
render(<Search products={[{id:"a",name:"Apple"}]}/>);
await user.type(screen.getByRole("searchbox", {name:/search/i}),"apple");
expect(screen.getByText("Apple")).toBeVisible();
~~~
Search, React testing libraries and test runner must be installed. This is not a standalone runnable test.

**Security:** User-supplied HTML requires sanitization and no unsafe `dangerouslySetInnerHTML`; browser XSS and server authz are separate concerns.

## Release evidence and risks
Check installed framework and dependency versions first. Run deterministic negative cases, a real production build and relevant browser interactions. Treat tokens/identity/cookies and tenant data as untrusted across any HTTP or serialized-client boundary. Record untested behavior rather than inferring production guarantees from documentation or mocks. Ensure error and empty states, cancellation and loading are part of the expected contract.

## Official references
- https://testing-library.com/docs/react-testing-library/intro/
- https://react.dev/reference/react-dom/client/hydrateRoot
- https://playwright.dev/docs/intro
