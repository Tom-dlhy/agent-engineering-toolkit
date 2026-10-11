# Motion review — evidence-led rubric

**Read when:** reviewing a motion PR, diagnosing "feels sluggish" reports or evaluating visual interaction polish.

## Inspect implementation and intent

For each animated element record: trigger, user purpose, frequency, framework/primitive, property list, duration, easing, exit, interruption path, reduced motion support and how the semantic state is announced.

### Review scoring table
| Dimension | Pass | Common failure |
|---|---|---|
| Justified behavior | Motion clarifies an observable change | Decorative movement on a high-frequency task |
| Spatial story | Enter/exit direction consistent with origin | Popup flying from unrelated edge |
| Timing | Feels responsive for user task | 500ms menu exit blocking navigation |
| Property performance | No pathological layout/repaint on tested device | Every-frame JS geometry or large blur |
| Interruptibility | Rapid open/close doesn't leave stale state | Completion callback overrides latest state |
| Keyboard/AT | Focus and reduced-motion correct | Invisible focusable dialog during fade |
| Consistency | Reuses approved motion tokens | One-off easing per screen |

## Find bugs, not aesthetic absolutes

Severity: blocking when a user cannot act or focus, high when motion triggers significant accessibility/performance harm, medium when recurring delay harms flow, low when minor polish. Always cite file/line, reproducible input, expected outcome and why the current behavior fails; distinguish preference from proven defect.

## Concrete QA route

1. Review code paths and defaults for each key state.
2. Trigger via pointer and keyboard, rapidly alternate actions and navigate away mid-animation.
3. Toggle reduced-motion and check content/focus state.
4. Compare mobile/touch and slow CPU; profile when performance is alleged.
5. Re-review after minimal fix; avoid unrelated redesign.
6. Report observed vs not-tested scenarios.

## Responsible adaptation

The high-craft inspiration derives from https://github.com/emilkowalski/skills/blob/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/review-animations/SKILL.md . Do **not** copy the upstream command's automatic output-format or first-response instructions. A local UI review may require a report format chosen by the user or repository.
