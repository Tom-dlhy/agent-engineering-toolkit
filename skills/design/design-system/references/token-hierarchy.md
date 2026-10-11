# Design system — token layering and component contracts

**Read when:** implementing a reusable token architecture or migrating themes across an actual UI library.

## Four-level token model

1. **Primitive**: named color ramps, numeric spacing scale, font families/weights, radii, motion curves.
2. **Semantic**: background, surface, foreground, border, accent, danger, success, focus, disabled. Roles are stable even when palette changes.
3. **Component**: button-primary background, dialog surface, input-error ring; values normally alias semantic tokens rather than introducing fresh arbitrary colors.
4. **State and mode**: hover, active, disabled, focus-visible, invalid, light/dark, high-contrast and reduced-motion.

Example CSS layer:

~~~css
:root {
  --color-ink-900: #17263a;
  --color-paper-050: #faf9f6;
  --surface: var(--color-paper-050);
  --foreground: var(--color-ink-900);
  --button-primary-bg: var(--color-ink-900);
  --button-primary-fg: var(--color-paper-050);
}
[data-theme="dark"] {
  --surface: #17263a;
  --foreground: #faf9f6;
  --button-primary-bg: #faf9f6;
  --button-primary-fg: #17263a;
}
~~~

Illustrative sample, not a reviewed accessible palette for production. Check contrast of each actual text/interactive pairing. Avoid semantic token name collisions with library-generated variables unless intentional.

## Component specification

Define public API, anatomy, variants, size, loading, disabled, invalid, keyboard, focus, pointer/touch, error, empty and reduced-motion behavior. Example: Button has action semantics; a styled anchor navigates. Select needs controlled/uncontrolled value schema. Dialog defines focus return and dismissal. Source-owned component libraries require keeping generated sources as maintained project code.

## Provider integration

- For shadcn/UI custom source, inspect components.json and underlying Base UI vs Radix before altering slots.
- For MUI/Chakra/Ant/Prime/Mantine, map semantic tokens into provider-supported theme APIs and avoid global CSS overrides that fight library layers.
- For native Flutter/React Native, token names can be shared conceptually but application mechanisms and units differ.

## Migration plan

Snapshot current public variants; introduce aliases first; migrate representative form/dialog/table; stage unused token removal only after consumer audit and visual regression checks. Test hydration, contrast, dark/light and forced-colors when relevant.

Guidance informed by independently reviewed design-system source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/67803eac81607188194aea9842a723b89326d90d/.claude/skills/design-system/SKILL.md . No source code or token data has been vendored.
