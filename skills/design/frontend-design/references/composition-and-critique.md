# Frontend design — composition and implementation QA

**Read when:** translating a design direction into a responsive page, editing information hierarchy or critiquing screenshots/code.

## Build from actual content

1. Write the information order: user goal, answer, supporting evidence, next action.
2. Inventory and reuse site-wide tokens, component primitives and layout containers.
3. Establish a limited visual scale (heading/subhead/body/caption, large/medium/small spacing) rather than dozens of one-off values.
4. Place content on deliberate grid axes; use asymmetry only when reading order remains clear.
5. Design image cropping based on subject and breakpoint. A generic stock hero is not a substitute for correct source material.
6. Implement loading, disabled, no-results, error and long-content states; polish the task flow, not only the hero.
7. Test visually with a rendered browser across mobile/tablet/desktop, at text zoom and dark/light when applicable.

## Example: section hierarchy

A section containing a step-by-step order process needs a clear title, numbered steps with strong labels and one main action. A card grid with equal-weight decoration for every sentence obscures progression. Make action states and contact method explicit; verify form accessibility and error recovery.

## Visual QA before release

| Dimension | Evidence |
|---|---|
| Content | No placeholder/invented claims; labels reflect actual product |
| Hierarchy | One dominant focal point per section; heading structure matches reading order |
| Spacing | Consistent rhythm; no accidental density jumps or misaligned baselines |
| Responsive | Long labels and narrow viewports do not overflow; image crop preserves subject |
| Interaction | Keyboard focus, disabled/error/empty/loading states coherent |
| Performance | Correct image sizes, CSS layout stability, no unnecessary motion costs |
| Brand | Colors, type, icons, imagery and tone belong to same identity |

Separate defects from preferences, reference specific viewport and selector/element. Never report screenshot QA performed when only source code was inspected.

## Collaboration

If token/semantic contrast is the root issue, route to design-system. If motion or transitions are dysfunctional, route to interaction-motion. If the user cannot complete the task, route to ux-audit. Provider-specific props go to UI provider skill, not a generic redesign.

Methods adapted from design engineering sources with independently written examples: https://github.com/emilkowalski/skills/blob/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/emil-design-eng/SKILL.md .

## Browser review must be evidence-based

Capture and compare real rendered screens at the project's target
viewport sizes and browser engines before claiming visual polish.
Critique **content first**: page purpose clear in first screen, genuine
features rather than invented KPIs, one legible action hierarchy,
appropriate density and clear error/recovery messages. Then examine
typographic baseline alignment, contrast/focus, image crop, clipped
localization, overlay portals, z-index, desktop/tablet/mobile, 200%
text zoom and reduced motion. Record exact route/viewport/element
and proposed correction instead of a subjective overall score.
For component-level audit use the official Vercel Web Interface
Guidelines at https://vercel.com/design/guidelines and W3C APG
https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ .
