# UI provider compatibility, ownership, licensing and runtime gates

Read when: comparing source-owned, headless and styled UI providers or selecting a component library in a framework-specific project.

## Identify the true integration surface
An existing shadcn app usually owns local component source; inspect `components.json`, installed local `components/ui` files, package lock and chosen primitive family. Base UI, Radix Primitives and React Aria can be **headless foundations**, while a styled library provides another API/ownership model. Do not promise switching primitives is only a dependency bump.

As of July 2026, **new shadcn projects default to Base UI**, yet official docs explicitly retain Radix support and say existing Radix applications do not need to migrate. This is a current default for **new** projects, not an instruction to rewrite deployed apps. Source: https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default

## Selection matrix
| Question | Compare with real docs | Pitfall |
|---|---|---|
| Framework/SSR/mobile | Supported framework/major, RSC/SSR/hydration, native vs web | Assume React-only component works in Vue/Flutter |
| Primitive semantics | Composite slots, focus model, keyboard handling, portals | Copy Radix `asChild` into Base `render` APIs |
| Styling ownership | Theme tokens, CSS-in-JS/Tailwind, source ownership | Install a second global token system |
| Product complexity | Basic form vs enterprise DataGrid, editing, virtualization, charts | Assume `Table` equals paid/licensed DataGrid |
| License/plan | MIT/open-source package vs separately licensed Pro/Premium widgets | Treat a demo as free production feature |
| Maintenance | Upgrade churn, local forks, dependency graph, design tokens | Blind registry overwrite of local customizations |
| Accessibility/RTL | Actual accessible composition and supported locales | Assume marketing "accessible" automatically means WCAG AA |

Provider *existence* differs from provider *fit*. For React with rich forms/permissions/keyboard-heavy enterprise tables, exercise actual DataGrid or combobox behavior; for a static brochure site, avoid installing an enterprise framework simply to show buttons.

## Proof and boundaries
Before changing the chosen package, define sample Form + Dialog + data display + color scheme and mobile keyboard test. Source-only accessibility promises do not establish actual AT behavior. MUI X license tiers and shadcn local source require separate attention to upgrades and optional chart examples; no new chart engine or UI kit to solve a visual-encoding decision.

Official: https://mui.com/x/react-data-grid/ and https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default and https://react-spectrum.adobe.com/react-aria/
