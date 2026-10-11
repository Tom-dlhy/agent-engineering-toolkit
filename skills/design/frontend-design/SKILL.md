---
name: frontend-design
domain: design
version: "2.0.0"
description: >-
  Use when establishing or significantly improving the visual direction, composition and distinctive UI craft of a web interface or landing page. Do not replace an established brand or add generic visual trends to a small bug fix.
---

# Frontend design — visual intent before styling

## Discovery and decisions

1. Inspect actual brand guidelines, content, target reader, existing screens and component tokens; preserve visual identity and verified business details.
2. Classify task: new page, redesign, incremental polish or audit. A redesign should preserve user workflows and validated strengths unless requested otherwise.
3. Name the target design language in concrete terms: typography behavior, grid, color roles, image direction, density, hierarchy and interaction tone. Explain how it serves audience and product.
4. Reject template-shaped work that doesn't serve the brief: gratuitous dark dashboards, enormous repeated cards, meaningless purple gradients, invented testimonials or decorative charts.
5. Build using the installed component library and layout system. Ensure semantic HTML, contrast, keyboard, state feedback, responsive content and performance.
6. Validate real screen sizes and loading/empty/error states; a code-only review is not visual QA.

## Two-pass anti-template review before building a new page

For a substantial new UI or redesign, write a **brief-grounded** micro-direction:
audience and task, real content/constraints, a small token palette,
type hierarchy, composition/wireframe, deliberate media and interaction
style. Critique it against a different page for the same industry: if it
would fit any generic SaaS, explain what to change **before coding**.
Preserve an approved brand; do not ban a font, gradient, bento or
minimalism categorically. Distinctiveness is the product of intentional
choices, not decorative complexity. Ask for existing brand/assets only
when unavailable and actually essential, otherwise state grounded
assumptions and proceed with the supplied context.

Provider component skills own library APIs. For the **appearance** of a
whole page, route here before a library cookbook; for a bug fix, do not
redesign the brand.

## Deep routing

- [Brief to deliberate art direction and acceptance](references/brief-to-art-direction.md) — **read when** designing a new multi-section experience, choosing visual voice, or preventing generic template drift.
- [Visual direction, brand specificity and anti-template diagnosis](references/visual-direction-and-anti-slop.md) — **read when** a page feels generic, when deriving visual direction, or when designing/revising a marketing/product surface.
- [Compositional execution and visual QA](references/composition-and-critique.md) — **read when** implementing layout/hierarchy, reviewing screenshots, avoiding visual regressions or explaining polish improvements.

## Collaboration

Use design-system for token architecture, typography-layout for type/grid tuning, interaction-motion for motion, ux-audit for usability evidence, and brand-identity-visualization for requested identity boards.

## Completion standard

A grounded design rationale, interface changes that reuse project constraints, concrete states, and an honest report of screen/browser checks actually performed. No forced aesthetic, no unapproved brand overhaul.
