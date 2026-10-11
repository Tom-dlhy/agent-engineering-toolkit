# Visual design research — palette, density and product fit

**Read when:** choosing typography/palette/style direction from a product brief or diagnosing mismatched tokens. Not required when a known brand palette is already approved and unchanged.

## Avoid the style lottery

UI/UX Pro Max collects styles, palettes, typography and guideline data, but this toolkit intentionally does **not** load a 800-file corpus or execute its search.py script on every design task. Use a short decision record, refer to version-pinned upstream data only when necessary, and record why a suggestion fits the product rather than blindly accepting search hits.

## Decision dimensions

| Dimension | Questions | Result to record |
|---|---|---|
| Product domain | Financial/health/consumer/creative/public sector? | Trust, formality, imagery constraints |
| Audience and task | Scanning complex data or browsing editorial content? | Density, hierarchy, type emphasis |
| Brand | Existing logo/fonts/palette approved? | Preservation vs exploration boundary |
| Visual rhythm | Many forms, tables, images or long-form text? | Spacing and component defaults |
| Interaction | Touch, accessibility, high contrast, locale? | Focus/touch/error requirements |
| Maintenance | Source-owned or theme provider? | Real token architecture and upgrade cost |

## Practical palette creation

1. Start with a neutral foreground/surface relationship that actually supports body reading, forms and error states.
2. Pick one primary action/accent; give danger/success/focus functional roles independent of branding.
3. Derive light/dark modes with contrast checked on text, borders, disabled states, status colors and control focus.
4. Add decorative color only when it reinforces information architecture. Avoid a five-color palette where every shade competes as a primary CTA.
5. Compare color pairings in actual content and mobile device brightness, not isolated swatches.

A palette designed for a travel editorial brand may emphasize photography and warm surfaces; a dense enterprise dashboard may need a more restrained functional ramp. Neither should be forced into the same purple-gradient "AI SaaS" treatment.

## Verification

Render representative page/form/data states; use an accessible color contrast checker and inspect forced colors if target platform requires it. Record why alternatives were rejected and what was measured.

Research reference: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/67803eac81607188194aea9842a723b89326d90d/.claude/skills/ui-ux-pro-max/SKILL.md . This is a curated **methodological adaptation**, not a complete mirror of its dataset or claim that its exact counts remain stable.
