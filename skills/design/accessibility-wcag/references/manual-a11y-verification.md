# Manual accessibility verification and evidence

Read when: producing a test matrix or proving a remediation across keyboard, screen readers, viewport reflow and alternative color/motion preferences.

## Minimal journey-oriented matrix
Define affected route, critical task, expected accessible behavior, platform + browser + versions, tester and results. A representative manual suite includes:
- Keyboard-only navigation without mouse, from start through error/success and modal/menus. Record any focus trap, hidden focus, shortcut conflict or unreachable content.
- Screen reader on at least one relevant actual platform (for example NVDA + Windows browser or VoiceOver + Safari) when access permits. Verify spoken label/role/value, grouping, status and error; report missing coverage explicitly.
- Browser zoom 200% text resize; 400% for reflow use cases; 320 CSS px equivalent checks, with appropriate WCAG exceptions for essential two-dimensional content.
- Forced-colors/high contrast, reduced motion, responsive input method and orientation where relevant. Check state transitions and feedback.
- Automated axe/lint as additional smoke check, not a certificate.

## Regression example
```text
ID: A11Y-12
Surface: reservation form, /book
Precondition: invalid date and modal confirmation visible
Steps: keyboard Tab -> submit -> inspect error -> correct -> confirm -> Escape
Expected: focused error or summary, understandable message, modal focus containment and return
Result: PASS only after actual run, evidence browser/OS and screenshot/recording ID
Untested: screen reader, iOS hardware keyboard
```
Evidence should be privacy-safe: no user-entered secrets, names or personal data in screen recordings or stored fixtures. For screen-reader runs, include spoken sequence notes rather than declaring "works with screen readers" from ARIA attributes alone.

## Claims and exit criteria
Sort issues into observed failure, probable risk, and unsupported hypothesis. Map confirmed defects to normative criteria only after verifying the wording/level. An internal accessibility review is not third-party certification; passing a checklist or an axe scan cannot prove complete WCAG conformance.

Official sources: https://www.w3.org/WAI/test-evaluate/ and https://www.w3.org/TR/WCAG22/
