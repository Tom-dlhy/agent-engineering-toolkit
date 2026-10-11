---
name: design-system
domain: design
version: "2.0.0"
description: >-
  Use when constructing, migrating or auditing a product design system with reusable tokens, semantic themes and accessible component contracts. Do not create a competing system for an existing stable component kit or one-off styling change.
---

# Design system — coherent reusable decisions

## Inspect before inventing

1. Inventory existing brand assets, tokens, CSS variables, component providers, theme architecture, spacing/type scales and component variants.
2. Distinguish raw primitives from semantic aliases and component/state tokens. Map required UI roles before selecting aesthetic palette values.
3. Choose the actual system to extend (shadcn, MUI, Mantine, Chakra, custom etc); avoid loading all UI providers or creating a parallel global theme.
4. Define tokens in light/dark and high-contrast contexts with a11y checks, then validate realistic form, dialog and data views.
5. Document ownership, change control, deprecation/migration and version compatibility. Avoid "design system" as a collection of screenshots only.

## Relevant deep expertise

- [Primitive, semantic and component token architecture](references/token-hierarchy.md) — **read when** defining/designing tokens, variants, component interfaces or migration strategy.
- [Style research and palette decisions](references/style-research-and-palette.md) — **read when** choosing a coherent visual vocabulary, palette roles and product-specific design directions using curated comparative examples.

## Interfaces

Use typography-layout for type/grid detail, ui-library-selection to choose a provider, frontend-design for an individual composition, brand-identity-visualization for a conceptual board.

## Done

A small set of portable semantic decisions, representative accessible components/states, implementation files in the chosen stack and evidence of visual/functional verification.
