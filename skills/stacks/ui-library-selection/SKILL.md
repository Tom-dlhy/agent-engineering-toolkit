---
name: ui-library-selection
domain: stacks
version: "3.0.0"
description: >-
  Use when choosing or comparing UI component libraries or design systems across React, Vue, Angular, Svelte, mobile and Flutter, including an explicitly requested migration. Do not use to implement components in an already selected provider, choose a chart's visual encoding, or redesign an established product because another library is trendy.
---

# UI library selection — provider fit and ownership, not implementation

## Inspect, filter, prove
1. Inspect lockfile/manifests, current UI components, `components.json` (when shadcn), theming/tokens, installed primitive strategy, framework/SSR/native environment and existing customization. **Retain a healthy already installed provider** unless a functional requirement justifies migration.
2. Separate **headless primitives**, **styled systems** and **source-owned components**. shadcn/ui is source-owned and its underlying primitives may differ (Base UI/Radix/others supported by the installed release); never equate its wrappers with a standalone Base UI package or assume every library ships a chart engine.
3. Decide required component **capabilities**, not library marketing: complex forms/dialogs, advanced DataGrid license/row models, accessibility and keyboard behavior, RTL/i18n, token/brand control, mobile/native, SSR/hydration, testing hooks and upgrade cadence.
4. Reject incompatible framework/major release, required license tier or unsupported platform before scoring style and speed. Shortlist at most three **compatible** choices with current official docs and exact version/plan caveats.
5. Proof with a realistic **Form + Dialog + navigation + data view + theme**. Inspect framework providers and component contracts; automated checks do not substitute for actual keyboard/screen-reader and mobile QA. Compare accessibility of the configured application, not vague claims that a library is automatically compliant.
6. Quantify migration cost: replacement count, token mapping, forms/state semantics, layout and API ref changes, regression screenshots, design ownership, vendor lock-in, paid components and ongoing upgrades. Avoid mixing providers unless a specific compositional boundary makes it necessary.
7. Record recommendation, rejected candidate and release/rollback method. Never install or overwrite source-owned components from a selection request alone.

## References (load only for choice/migration)
- [Provider comparison and official documentation index](references/library-map.md) — **read when** discovering/selecting framework-compatible libraries; not API implementation instructions.
- [Component ownership, runtime compatibility and licensing](references/compatibility-and-license-gates.md) — **read when** comparing primitives, source ownership, paid DataGrid, framework major versions or runtime constraints.
- [Migration proof and progressive library adoption](references/migration-and-component-proof.md) — **read when** replacing a current library or validating actual component fit on representative interactions.

## Contracts with other skills
`skills/ui/<provider>` owns **installed** component APIs and real chart/grid behavior, `ui-component-research` owns specialized component correctness, `design/design-system` owns tokens, `design/data-visualization-design` owns *what graphs mean*, and `stack-advisor` coordinates the whole architecture. Do not activate all UI providers or force migration because a vendor changelog changes defaults.

## Exit
Chosen provider/primitive/version and ownership model, realistic representative component evidence, accessibility/license constraints, estimated migration effort and documented known unknowns.
