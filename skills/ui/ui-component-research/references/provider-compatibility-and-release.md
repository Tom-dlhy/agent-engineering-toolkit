# Component-provider compatibility, upgrades and release evidence

**Read when:** migrating a UI library, changing primitive backends,
shipping complex controls or claiming production-ready behavior.

## Inventory before touching a dependency
Record installed package + lockfile version, framework, copied local
component source, styling engine, icons and providers. Determine
whether the product uses source-owned shadcn/gluestack, headless
Radix/Base/Bits/React Aria, styled MUI/Prime/Chakra, CSS-only
daisyUI or native Flutter/React Native widgets.
This determines who owns accessibility, CSS and breaking upgrades.

## Exact API, legal and migration boundaries
Check official **version-matched** component anatomy, migration and
license before implementing. Radix asChild and Base render are distinct;
Chakra v2 flat parts and v3 compound parts differ; HeroUI v2/v3
requirements and packages differ; Skeleton warns of Tailwind
incompatibility with Flowbite/daisyUI; MUI X Community vs Pro/Premium
features have different licenses. Avoid forcing an upgrade to use one
showcase demo. Unknown props are documented as unknown, not invented.

## User-facing release contract
Record native element/role/name, keyboard, pointer and touch, state
ownership, disabled/readonly, selected/invalid/busy, validation,
async cancellation, i18n/RTL, modal portal/focus return and SSR/native
lifecycle. For data-heavy tables use stable row ID, server paging,
filter and selection rules.

A modal according to W3C APG requires correct initial focus,
keyboard containment, Escape and logical restoration. Changing
a rendered button to a noninteractive div merely for visuals can
break these behaviors. Check screen-reader announcements.

## Visual fidelity is a different responsibility
Use frontend-design for product-brief-specific art direction; this
UI skill handles semantics, API and integration. Vendor themes and
demo layouts are **scaffolds**, not proof of brand-specific design.
Ensure owned design tokens, typography and actual product content
are reflected in components without removing focus, contrast,
disabled, error and empty states. Test real narrow screens,
text expansion and both themes where applicable.

No automated text heuristic can determine whether a page looks
AI-generated. Perform an informed human visual critique of
rendered screenshots against the concrete brand and task.

## Evidence and limitations
Run installed version typecheck/build, component interaction tests
and real browser (or native device) keyboard/touch, focus and state
tests. Record what ran and what could not be verified. This
guide itself proves no dependency compatibility, production
accessibility or visual originality.

## Official sources
- https://base-ui.com/react/handbook/composition
- https://github.com/shadcn-ui/ui/blob/main/skills/shadcn/rules/base-vs-radix.md
- https://chakra-ui.com/docs/get-started/migration
- https://mui.com/x/introduction/licensing/
- https://www.skeleton.dev/docs/svelte/get-started/installation
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
