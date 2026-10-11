# Test findability and migrate navigation safely

Read when: reworking an existing live product taxonomy, conducting navigation experiments or updating routes and bookmarks.

## Evaluation protocol
Create task descriptions without the answer embedded. Start with known user goals and a text-only navigation tree. Ask users where they would look, record first choice, backtracks, direct/indirect success and time where collected. Use actual participants only when privacy, consent and sampling permit; otherwise mark as an **internal heuristic tree walk**, not empirical user evidence.

```text
Task: "Find the most recent payment receipt."
Tree: current vs proposed menus (no visual styling distractions).
Measures: first selection, correct destination, detours, misunderstandings.
Do not claim: "85% findability" without real participant counts.
```
If analytics are available, verify what events mean, population and privacy before drawing conclusions.

## Migration contract
Map old destination -> new destination, stable IDs, redirects (when relevant), deep links, locale path compatibility, permissions, navigation labels, UI test selectors and analytics continuity. Update breadcrumbs, internal links, search indices and sitemaps **only in coordination with** the relevant frontend/SEO owner. No mass redirect changes without explicit approval and rollback plan.

## Negative checks
A user with no permission cannot view hidden object names through menus, search or destination errors; old shared links degrade gracefully; no orphaned content; multiple locales remain navigable; mobile menu and keyboard order match hierarchy.

References: https://design-system.service.gov.uk/patterns/navigate-a-service/ and https://www.w3.org/WAI/test-evaluate/
