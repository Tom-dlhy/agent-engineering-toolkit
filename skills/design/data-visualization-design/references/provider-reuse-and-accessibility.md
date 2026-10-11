# Reuse installed chart providers; accessibility and release contract

Read when: turning a chart specification into a component handoff, evaluating an existing UI chart or ensuring visualizations work without inaccessible mouse-only interaction.

## Non-negotiable reuse ladder
1. Inspect `package.json`, lockfile, source imports and installed UI library's own chart examples and components. Reuse the same chart package and design tokens.
2. If using **shadcn**, its Chart is a source-owned composition atop **Recharts**; inspect local `components/ui/chart.tsx`, project `components.json`, Recharts major version, `ChartConfig`, `ChartContainer`, tooltip/legend primitives and existing theme CSS. Official: https://ui.shadcn.com/docs/components/chart and https://ui.shadcn.com/docs/components/base/chart. Do not create a second chart wrapper merely because a template looks different; do not copy code for an incompatible Recharts major.
3. If using **MUI**, inspect installed `@mui/x-charts` tier/version, components and upgrade/license constraints. Official: https://mui.com/x/react-charts/overview/ . Avoid assuming all Pro/Premium chart options are Community features.
4. If using **Base UI**, know that `@base-ui/react` provides **unstyled accessible primitives**, not a guaranteed chart rendering engine (https://base-ui.com/react/overview/about). shadcn can use Base UI primitives and charts still come from Recharts. Do not tell the agent to import imaginary chart components from `@base-ui/react`.
5. If using another UI provider or chart system, inspect its installed API and official documentation, not a substitute provider. Route exact code work to `skills/ui/<provider>` or the actual chart package documentation.
6. Add a new dependency **only** when required capability is genuinely absent, implementation is authorized and licensing, SSR, security, performance and maintenance have been compared. Consult `stacks/ui-library-selection` only for a real selection decision; do not browse/install all chart packages.

## Visualization acceptance contract (independent of vendor)
- Each chart communicates a specific question and sourced values, with visible axes/units/date range, intelligible legends and truthful defaults.
- Complex graphics need a concise description plus an accessible equivalent of the essential information; a nearby semantic table or structured description is often suitable. Tooltips alone do not satisfy users who cannot hover. https://www.w3.org/WAI/tutorials/images/complex/
- A meaningful data table uses header associations; see https://www.w3.org/WAI/tutorials/tables/ . Don't dump the complete dataset into `aria-label`.
- If chart is interactive, test keyboard/touch access to the same information/filters, announce query-state changes appropriately, and prevent false selection on loading.
- Apply existing semantic tokens, avoid relying only on color, verify forced colors/contrast, dark mode and responsive labels; respect reduced-motion preference for optional animation.
- Measure actual rendering and verify real controls in a browser when available, rather than claiming a static screenshot proves accessibility.

## Handoff example
```text
Task: Plot weekly resolved tickets in the existing React dashboard.
Design decision: comparison bars, zero baseline, week labels, gaps as missing.
Metric owner: existing analytics view, no new business formulas.
Renderer: existing shadcn Chart + installed Recharts.
Implementation owner: ui/shadcn-ui and exact current local component.
QA: narrow/desktop, keyboard, screen reader/table alternative, filter/error state.
Do not: npm install MUI X, implement canvas renderer, or copy new Recharts docs over local v2.
```
The example specifies responsibility but not copy-paste implementation code. Versioned APIs always come from the selected provider.
