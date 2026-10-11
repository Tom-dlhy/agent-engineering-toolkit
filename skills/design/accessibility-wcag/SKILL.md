---
name: accessibility-wcag
domain: design
version: "0.1.0"
description: >-
  Use when implementing or auditing keyboard navigation, semantic markup, form errors, focus states or WCAG accessibility requirements. Do not claim certification from automated checks alone.
---

# accessibility-wcag

## Core checks
Audit semantic heading and landmark structure, labels/names/roles, focus order, visible focus, contrast, keyboard-only navigation, motion alternatives, zoom and touch targets.
## Interactive patterns
Dialogs require focus management, escape and return-focus. Forms need programmatically associated errors, validation that does not rely solely on color, and clear recovery. Dynamic updates may need live-region announcements.
## Verification
Run automated checks (e.g. axe) for common issues, then manual keyboard testing and representative screen-reader flows. Include narrow viewport and 200% zoom. Differentiate accessibility defects from subjective style.
## Governance
Record user impact, affected guideline when confidently known, fix and test evidence. Reassess after component library updates.
