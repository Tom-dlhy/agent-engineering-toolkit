# Motion design — should this animate?

**Read when:** selecting motion behavior for a flow or auditing whether an animation helps rather than distracts.

## Identify the user job first

Motion should convey feedback (press or successful action), relationship (a panel opened from a trigger), state (selection), progress (navigation) or occasional delight. Ask whether the same information remains clear when animation is disabled. If not, add a static affordance first.

## Frequency as a heuristic, not a law

| Interaction | Typical goal | Default direction |
|---|---|---|
| Keyboard shortcut, command palette, rapid repeated toggle | Speed and continuity | Usually instant; test whether motion costs more than it explains |
| Hover/focus/checkbox | Confirmation | Very restrained state change, no moving content |
| Dialog, sheet, navigation transition | Spatial origin and state | Short enter/exit with consistent direction |
| First-use onboarding / intentional celebration | Orientation or delight | Expressive but dismissible and nonblocking |

A blanket frequency threshold cannot prove an animation is wrong: measure user speed and preference. Respect reduced motion and different input modalities; keyboard activation may deserve immediate response even if pointer navigation uses transition.

## Spatial grammar

Objects should originate from believable anchors. A popover appearing under its trigger should not fly in from the opposite corner. Keep enter/exit direction consistent with navigation direction and information hierarchy. Overlays must not obscure the triggering control before keyboard focus is transferred.

For an accordion, consider whether motion of content height improves scanning; native disclosure without transition may be better for high-frequency forms.

## Design review experiment

Try the same journey in two states: transitions disabled and proposed motion. Record time-to-action, comprehension, focus behavior, perceived delay and user preference if test participants exist. Simulate repeated use, not only first impressions.

## Failure and ethics

Avoid animating financial totals, form validation, destructive confirmation or live dashboards merely for flair. Excessive parallax can cause nausea; prolonged motion can interfere with assistive technology and working memory. User preference beats the author's signature aesthetic.

Source inspiration, rewritten for this toolkit: https://github.com/emilkowalski/skills/blob/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/animate/SKILL.md . No upstream prompt wording is redistributed.
