# UI production quality — provider correctness without generic AI pages

Date reviewed: 2026-10-11. This is a **procedural guide**, not another
skill. The repository already routes intentional visual identity to
frontend-design and exact component API to the selected UI library.
Do not install or invoke external skills automatically.

## Three separate quality gates

### Gate A — correct library and operational contract (blocking)
- Identify framework, runtime, provider name and installed major from
  lockfile and actual imports. Do not recommend a new component kit when
  one already supports the task.
- Read exact provider release notes and anatomy; distinguish styles and
  behavior: Base render vs Radix asChild, React Aria slots, MUI license,
  Vue vs Angular bindings, CSS-only daisyUI, native RN/Flutter.
- Specify label/role, default/controlled value, events, required props
  and semantics. UI type signatures do not validate remote user input.
- Test keyboard and focus/return, disabled/read-only/invalid, loading,
  empty, errors, long labels, i18n/RTL if relevant, touch, zoom,
  dark/light where used, and SSR/hydration or native lifecycle.
- Check WAI-ARIA APG against dialog/combobox/table pattern and WCAG 2.2:
  Target Size Minimum 2.5.8 AA is generally 24×24 CSS px with documented
  exceptions; it is NOT an unconditional 44px legal minimum.
- Treat paid MUI X features and third-party source-owned registries as
  dependency/legal review before inclusion.

### Gate B — real product visual direction (brief before generation)
- Record **audience, primary task, factual content, brand constraints**,
  media rights, existing UI, target devices and tone.
- Define a compact art direction *before coding* (typography roles,
  semantic colors, layout axes, density, image treatment, motion).
- Counterfactual: remove brand name and logo. Would this page work
  unchanged for any generic AI SaaS? If so, name and fix the **specific**
  missing product signal (workflow, local imagery, real service
  commitments, taxonomy, meaningful data relationships).
- A cliché is a **mismatch**, not a forbidden CSS feature. Inter or a
  white background can be the right solution for a brand or functional
  B2B tool. Don't force maximalism, serif display, noise texture,
  gradients or asymmetric layouts without justification.
- Avoid invented metrics, partners, testimonials and stock imagery
  represented as real people. Use explicitly marked placeholders.
  Make forms and data views useful before ornamental hero work.
- For a small patch, preserve approved brand and layout. Do not
  transform a one-button fix into a rebrand.

### Gate C — rendered design review and functional evidence
Inspect **actual screenshots** from running browser/native preview
at phone narrow, tablet and desktop target sizes. Compare original
and candidate at identical dimensions; inspect focus, 200% zoom,
overflow, text expansion, RTL (if needed), dark mode, scroll,
content cropping, loading/error/empty and reduced-motion settings.
Separate blocking UX/a11y defects from aesthetic preference.
Write issues with route, viewport, selector, reproduction and
proposed correction. No "looks premium" or unsupported 10/10 scores.

## Component selection / conflict matrix

| Task | Preferred owner | Avoid |
|---|---|---|
| Brand/art direction | design/frontend-design | Vendor demos as brand strategy |
| Token hierarchy | design/design-system | Per-component ad hoc hex colors |
| Typography/layout | design/typography-layout | Forced novelty instead of readability |
| Specific API/slots | one ui provider specialist | Cross-importing competing primitive APIs |
| Complex form/overlay/data grid | ui/ui-component-research plus provider | Handwritten fake ARIA controls |
| Library choice from requirements | stacks/ui-library-selection | Installing all UI frameworks |
| Accessibility acceptance | design/accessibility-wcag | Assuming library automatically passes every screen |
| Screenshot regression | design/responsive-visual-qa | Claiming QA from source-only review |

## Verified version pitfalls requiring explicit decisions

- shadcn: source-owned components.json and theme pairs; Base versus
  Radix backend changes trigger composition.
- Base UI: current package @base-ui/react, custom render prop/ref
  propagation; NOT Radix asChild.
- Chakra UI v3: compound component/provider/recipes vs v2 flat APIs.
- HeroUI v3: React 19+ and Tailwind 4; no blind mixing with v2.
- MUI X: Community MIT vs licensed Pro/Premium features.
- PrimeVue v4: styled token presets vs unstyled.
- Bits UI: Svelte 5 headless contracts.
- Skeleton: incompatible Tailwind feature overlaps with Flowbite and
  daisyUI according to official install docs.
- Mobile: React Native and Flutter require actual device talkback/
  voiceover/text scaling, not DOM aria screenshot simulation.

## Hand-off evidence format

**Direction:** one factual sentence about target user and task plus
token/type/layout rationale.
**Provider:** installed package+version; exact official component API.
**Changes:** source-owned components and brand tokens changed.
**Tests:** typecheck/build; specific real browser/native interaction
and screenshot viewports actually executed; a11y failures.
**Unknown:** APIs not verified in deployed version, unrun device/browser,
visual preference awaiting approval, licensing/upgrade risk.
**Rollback:** when existing vendor components or tokens are changed.

## Primary credible sources
- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- https://vercel.com/design/guidelines
- https://github.com/vercel-labs/web-interface-guidelines
- https://github.com/shadcn-ui/ui/blob/main/skills/shadcn/rules/base-vs-radix.md
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- https://docs.flutter.dev/ui/accessibility/accessibility-testing

External GitHub skill texts are inspiration/verification only and
are **not vendored or installed**; upstream license and provenance
would need explicit review for any future import.
