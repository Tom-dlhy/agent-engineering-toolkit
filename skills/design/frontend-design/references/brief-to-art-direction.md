# Brief to deliberate art direction — anti-template production method

**Read when:** a new product site, dashboard, editorial layout or redesign
needs a coherent and distinctive identity without sacrificing usability.

## Step 1: establish a factual creative brief
Capture real product job, audience, accessibility needs, preferred and
forbidden styles, existing visual identity, content/images, legal/brand
restrictions, actual call-to-action and top tasks. Do not invent press
mentions, revenues, performance metrics, partners, stock imagery "of the
team" or customer quotes. If material is unavailable, use an obvious
neutral placeholder; mark assumptions rather than assert fake facts.

## Step 2: design with controlled degrees of freedom
Make a small direction note before components:
- Brand voice in 3 adjectives grounded in offering (not "premium").
- **Palette:** 4–6 semantic colors with actual foreground/background
  pairs and contrast checked for normal/large text.
- **Typography:** display/body hierarchy, numerals, readability,
  line-length, weight and licensed font loading. Never change an
  approved font solely because a skill dislikes generic defaults.
- **Layout:** content-backed sections, reading axis, breakpoint grid,
  density and screenshot-sized rough wireframe.
- **Imagery:** genuine product/team/location or honest placeholders,
  crop rules and licensing; don't substitute generic SaaS visuals.
- **Motion:** one or two reasoned feedback/attention purposes; follow
  prefers-reduced-motion and avoid ubiquitous fade-up staggering.

## Step 3: anti-template counterfactual
Imagine replacing the logo/product name with another company. If
headline, cards, testimonials, colors and geometry still make equally
good sense, this is a weak art direction. Identify the **specific**
missing signal — source photo, service timing, price constraints,
workflow structure, data density, audience terminology — then change
that. Not every page needs asymmetry, serif headlines or textured
backgrounds. A financial dashboard can achieve differentiation
through honest data visualization, precise interaction and a clear
information hierarchy rather than theatrical ornament.

## Step 4: preserve UI component semantics
Build with the already-selected accessible provider and override
semantic tokens, not random CSS on each page. Choose correct
Dialog/Select/Tabs/Combobox semantics and focus model; do not turn a
button into clickable div to get a specific shape. Complex widgets
must support actual tab/arrow keys, disabled/invalid/empty/busy.
Show a content map from source field to visible UI so there are no
fictitious charts or placeholders surviving release.

## Step 5: visual critique and delivery proof
Check desktop (actual target width), tablet and narrow mobile,
200% zoom, keyboard-only flow, screen-reader name relationships,
both themes when supported, loading/error/empty states and text
expansion. Compare screenshots at same viewport before/after.
Track defect severity and fix, not one arbitrary "AI-slop score".

### Comparison: same library, two different appropriate outcomes
**Local maritime supply site:** an actual delivery window, product
categories and order process should dominate; meaningful place imagery,
real-world operating instructions and authentic color system.
**Analyst operations UI:** compact filters, clear table density,
audit status/errors and visible trust cues take precedence over
cinematic imagery. The same shadcn/React Aria/MUI primitives can
support both because visual intent comes from the product brief.

## Boundaries and evidence
The frontend-design skill owns art direction; design-system owns
semantic token architecture; ui-component-research and provider
skills own accessibility, exact API and integration; responsive-visual-qa
owns device screenshot regressions. Writing these instructions
does not constitute having run browser tests.

Primary guidance adapted in original words, not imported:
- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- https://vercel.com/design/guidelines
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
