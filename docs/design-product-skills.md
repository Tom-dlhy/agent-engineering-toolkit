# Design product experience expansion — create only autonomous responsibilities

Reviewed: 2026-10-11. Depends on Design content refactor PR #22.
Scope: **four new** narrow, provider-neutral skills. Existing design/UI/data/stack specialists remain authoritative for their own domains. No new category, no external skill vendoring, no charting dependency.

## Prior governance decisions (charter v2)

| Proposed skill | Decision | Unique job and trigger | Boundary / why not existing skill |
|---|---|---|---|
| `interaction-flow-design` | **CREATE** | Design an entire user task/journey with guarded state transitions and recoveries | `interaction-motion` owns animation; `ux-audit` inspects existing usability; `core/requirements-discovery` clarifies product constraints; UI providers own component behavior/APIs |
| `information-architecture` | **CREATE** | Organize content/menu/taxonomy/findability across destinations, search/facets, route migration | Not software architecture or `growth/content-strategy`; `frontend/<framework>` implements routes |
| `content-design` | **CREATE** | Form instructions, labels, inline feedback, errors, confirmations and product language | `growth/content-strategy` owns editorial program; `landing-page-design` owns public marketing story |
| `data-visualization-design` | **CREATE** | Pick truthful chart representation of existing verified data; visual encoding, uncertainty, alternatives | `data/analytics-modeling` owns metric truth, `ui/<provider>` owns components/chart API, `stacks/ui-library-selection` selects libraries only if none is adequate |

## Chart ownership contract — never duplicate providers

1. Inspect target project `package.json`, lockfile, `components.json` where applicable, existing chart components, CSS theme tokens and app constraints **before** selecting or implementing anything.
2. **Use existing charts first**. shadcn Chart is composed from Recharts. Its primitives may be Base UI or Radix, which does not change the chart engine. For MUI X use `@mui/x-charts` supported installed version, licensing tier and its docs. Other providers need their actual installed documentation.
3. `@base-ui/react` itself is an **unstyled accessible primitive library**, not an assumed chart engine. Never hallucinate `@base-ui/react` Chart APIs.
4. Never install Recharts, MUI X, visx, D3, Chart.js or another dependency merely because one has a pretty example. A new package needs an uncovered requirement, approved change, version/cost/license/SSR/safety justification.
5. Design owns **user question → chart family → axes/scales/units → visual hierarchy → text/table alternative**; Data owns **metric/aggregation calculations**; UI owns **how to render via the already installed provider**.
6. Every chart must have meaningful empty/loading/error/filter states, responsive and accessible information equivalence, not tooltip-only data access; real browser and screen-reader coverage must be reported, not assumed.
7. Separate comparisons of design quality from vendor feature comparisons; provider selection should not be reopened by a mere style preference.

### Grounded primary sources
- shadcn chart/recharts: https://ui.shadcn.com/docs/components/chart and https://ui.shadcn.com/docs/components/base/chart
- Base UI mission: https://base-ui.com/react/overview/about
- MUI X chart overview and license tiers: https://mui.com/x/react-charts/overview/
- W3C complex chart alternatives: https://www.w3.org/WAI/tutorials/images/complex/
- W3C accessible tables: https://www.w3.org/WAI/tutorials/tables/
- GOV.UK validation/error wording: https://design-system.service.gov.uk/components/error-message/
- GOV.UK service navigation: https://design-system.service.gov.uk/patterns/navigate-a-service/

Upstream websites support concepts and should be checked against the installed project version; no external snippets/scripts/third-party files have been copied into toolkit.

## Profiles / progressive context

`ui-ux-design` includes navigation, flows and microcopy as complementary daily disciplines; `product-launch` includes microcopy. **Data visualization is opt-in**, since many web apps do not contain graphs. No new chart providers installed or "universal dashboard" profile created. New references are local and only read on explicitly needed tasks.

## Verification and limits

Static tests cover registry unique entries (148 expected after this PR), profile budget, 38 Design leaf references, path-safe reads, lexical routing including negative provider cases and no code-level chart package scaffolding. `evals/design-product-routing.yaml` describes **unrun, model-driven held-out tasks**. Real screen-reader/browser charts, participant usability, true task completion improvement and measured token traces remain an evaluation backlog. Do not call static CI proof of visual quality.
