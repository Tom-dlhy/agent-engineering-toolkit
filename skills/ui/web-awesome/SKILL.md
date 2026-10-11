---
name: web-awesome
domain: ui
version: "2.0.0"
description: >-
  Use when implementing, integrating, debugging or reviewing Web Awesome components in a project that uses or has explicitly selected this library. Do not use for unrelated component libraries or to override an existing stack choice.
---

# Web Awesome — provider-specific UI engineering

**Best fit:** reusable standards-based Web Components across frameworks.
**Target stack:** HTML, React, Vue, Angular, Svelte, Astro.
**Official documentation:** https://webawesome.com/docs/

## Before changing code

1. Inspect package files / lockfile, framework version, theme provider and any existing components. Honor user-specified design system and the target project's rules.
2. Locate the **version-compatible official docs** for the specific component, including component anatomy, props, slots, events, CSS/theme hooks and examples. Do not infer APIs from another UI kit or from unversioned memory.
3. Examine existing project usage and prioritize reusable patterns; prefer an installed component over an added dependency. If not installed, justify the added dependency and its maintenance/licensing impact.
4. Choose controlled versus uncontrolled state intentionally; preserve the app's form, validation, routing, data-fetching and styling conventions.

## Component specialties

**Relevant component families:** Button, Dialog, Dropdown, Select, Input, Tab Group, Tooltip, Split Panel.

**Provider-specific method:** Identify the installed Web Awesome edition/version, component registration and theme CSS. Follow custom-element attributes/properties, emitted DOM events and framework-specific interop; check feature availability before assuming a Pro component.

For each requested component, write a small *component contract* before implementation: required imports and package version, compositional structure, relevant props/events, loading/empty/error/disabled states, keyboard and screen reader behavior, theme tokens, SSR/hydration or native lifecycle concerns, and representative official example. Consult the independent `ui-component-research` skill when component APIs or accessibility semantics are nontrivial; its detailed references are loaded only on demand.

## Guardrails and verification

Do not pass React/Vue props as though custom elements were native framework components. Verify SSR/hydration/custom-element registration and paid-feature constraints.

Test the behavior and keyboard flow, responsive/narrow layouts, focus and disabled states, contrast, form validation, reduced motion as appropriate, and current target framework integration. For advanced tables, test stable row identity, pagination/filtering, loading, empty and error states. For mobile, test actual platform semantics. Prefer vendor-supported solutions first, but do not misuse a component merely to avoid custom semantic markup.

**Done when:** component choice and API are justified with version-matched docs; the code reuses the project's design system; tests and visual/manual QA are reported accurately.
 
## Progressive expertise V2 — route instead of bulk-loading

- [Component mechanisms and patterns](references/component-patterns.md) — **read when** implementing Custom elements, Button, Dialog, Select, Theme, props/bindings, focus, state or interaction.
- [Integration, styling and verification](references/integration-and-verification.md) — **read when** configuring the library, SSR/native platform, themes, upgrades or testing.

Read only the needed leaf, in addition to the activated SKILL.md. Do not infer API compatibility from similar React/Vue/Angular/Svelte packages. A provider is opt-in and not automatically installed.

## Current provider contract and visual identity

Web Awesome custom elements require registration, property/event interop and styling across shadow roots, not React attribute imitation. Check edition/licensing and documented component availability; use brand CSS parts/tokens. https://webawesome.com/docs/
For art direction use the existing `frontend-design` skill; this specialist owns accurate library API, interaction, accessibility and version migration. Refine the existing brand rather than accepting a demo component theme as final UI.
