---
name: interaction-motion
domain: design
version: "2.0.0"
description: >-
  Use when designing, implementing or auditing interface motion, animation timing, gestures, transitions, micro-interactions or reduced-motion behavior. Do not animate frequently repeated actions without functional justification.
---

# Interaction motion — expert routing

## Decision order (do not skip)

1. Inspect existing interaction, user goal, existing motion tokens, framework, CSS/JS animation facilities and accessibility constraints.
2. Decide **whether** motion contributes feedback, spatial continuity, progress, state clarity or rare delight. If it doesn't, prefer no animation. High-frequency and keyboard-driven flows should be particularly restrained.
3. Pick the least expensive sufficient technique: CSS transition/animation for static changes, Web Animations API for imperative control, a motion library only for spring, drag, shared layout or complex interruption.
4. Choose properties, duration and easing based on spatial meaning, perceived frequency and available tokens; avoid invented rigid "one easing for all" standards.
5. Define cancellation, reversal, interruption, exit, rapid-click and unmount lifecycle explicitly.
6. Build accessible reduced-motion alternative and ensure functional feedback does not disappear.
7. Verify representative devices, keyboard paths and performance measurements before declaring polished.

## Targeted deep references

- [Motion necessity and decision framework](references/motion-decisions.md) — **read when** deciding what to animate, why, frequency and when to remove motion.
- [Easing, timing, CSS/WAAPI and springs](references/easing-and-implementation.md) — **read when** implementing motion, choosing tooling, timing, sequencing or transition primitives.
- [Interruptions, performance and accessibility](references/interaction-performance.md) — **read when** debugging jank, gestures, exits, reduced motion, focus and repeated transitions.
- [Motion review rubric](references/motion-review.md) — **read when** reviewing existing animations against user value and implementation correctness.

## Boundary

Use frontend-design for visual direction, ui-component-research for built-in Dialog/Popover lifecycle, and responsive-visual-qa for viewport screenshot validation. Do not add a third-party animation library for a trivial opacity transition.

## Deliverable

Explain purpose, selected technique, failure handling and observed checks; mark device/browser checks not run. Guidance is adapted, not copied, from Emil Kowalski's openly available design-engineering methods.
