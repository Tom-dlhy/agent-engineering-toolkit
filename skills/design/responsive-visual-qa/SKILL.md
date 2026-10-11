---
name: responsive-visual-qa
domain: design
version: "0.1.0"
description: >-
  Use when reviewing rendered frontend changes across desktop, tablet, mobile, zoom and UI states. Do not claim a visual QA pass from inspecting source code alone.
---

# responsive-visual-qa

## Matrix
Define representative browser widths and states: happy, loading, empty, error, long text, logged out/in and dark/light if applicable. Capture screenshots or use a real browser where tools permit.
## Inspect
Look for clipping, horizontal scroll, unreadable contrast, weak hierarchy, nonfunctional touch controls, broken overlays, sticky headers hiding content, image distortion and focus traps.
## Correct
Tie each finding to a reproducible viewport, action and visual symptom. Fix the smallest root issue in layout tokens or component CSS; avoid screen-specific magic numbers where possible.
## Evidence
Report actual viewports, browser/viewport tooling, checks run and unverified breakpoints. Automate screenshot comparisons when stable and cost-effective.
