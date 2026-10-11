---
name: ui-library-selection
domain: ui
version: "0.1.0"
description: >-
  Use when choosing, evaluating or migrating UI/component libraries across React, Vue, Angular, Svelte, native or Flutter projects. Do not use for an isolated component edit when the project's existing library is already decided.
---

# UI library selection

Select a library before writing components, **not by popularity but by project fit**. This skill complements `frontend-design` (creative direction) and does not replace the provider-specific skills.

## Determine the decision context

1. **Existing system first:** inspect framework, lockfile, imported UI libraries, tokens, design conventions and installed components. Do not replace an established system solely for preference.
2. **Requirements:** app category (marketing, dashboard, ERP, internal, mobile), level of custom branding, data/table complexity, accessibility/i18n needs, SSR, performance, licensing, CSS strategy and team familiarity.
3. **Preference class:** source-owned/open code (shadcn, gluestack), headless (Base UI, Radix Primitives, React Aria, Bits UI), styled (Mantine, MUI, HeroUI, Vuetify, PrimeNG), CSS/Web Components (daisyUI, Bootstrap, Web Awesome), mobile/native (Ionic, Paper, Tamagui, Flutter widgets).
4. **Compatibility gate:** shortlist **only** libraries compatible with the runtime, styling/SSR setup and current package versions. Verify latest compatibility against official docs; the catalog is a starting point, not a live compatibility guarantee.
5. **Decision:** compare 2–3 legitimate candidates on delivery speed, design freedom, a11y, complex component quality, ecosystem health, total ownership, license and migration cost. State the reason for one pick and one tradeoff.

Read `references/library-map.md` for candidates across frameworks. Do not load all provider skill bodies during selection.

## Handoff

Once the choice is explicit or the project already uses one library, load **only the matching provider skill** (`shadcn-ui`, `mantine`, etc.). For a complicated individual component also load `ui-component-research`. If two libraries are necessary, assign each a nonoverlapping responsibility and verify theme/overlay/focus interop. Do not install multiple competing component frameworks speculatively.

## Output

Report current stack, constraints, shortlist, selected library, rationale, compatibility checks, migration/maintenance costs, licensing assumptions and specialist skill to activate. For low-risk existing-project edits, reuse the current library without a new selection exercise.
