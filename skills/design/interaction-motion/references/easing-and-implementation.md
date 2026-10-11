# Motion engineering — easing, timing and implementation

**Read when:** writing CSS, WAAPI or library-driven animation, or selecting timing and sequencing for a specific UI event.

## Tool selection
| Requirement | Prefer | Why |
|---|---|---|
| Hover, focus, small state transition | CSS transition | Browser native and simple |
| Deterministic entrance independent of app state | CSS keyframes / supported starting-style | Small dependency surface |
| Imperative animation with cancellation | Web Animations API | Native timeline/control |
| Drag, velocity/spring, shared layout and complex exit | Existing approved motion library | Physics/composition where justified |

Check platform/browser support before using new CSS features and provide sensible fallback.

## Property cost

Compositor-friendly opacity/transform generally avoid layout work, but effects like blur, complex shadows or large translucent layers can still be expensive; test on devices. Height/width animation triggers layout and may be necessary for some accordions—don't claim a categorical ban. Use contain/content-visibility only when they don't break focus or sizing.

## CSS transition (small, real example)

~~~css
.panel {
  opacity: 0;
  transform: translateY(0.35rem);
  transition:
    opacity var(--motion-fast, 160ms) ease-out,
    transform var(--motion-fast, 160ms) ease-out;
}
.panel[data-open="true"] {
  opacity: 1;
  transform: translateY(0);
}
@media (prefers-reduced-motion: reduce) {
  .panel { transition-duration: 0.01ms; transform: none; }
}
~~~

A visually closed panel still needs real semantic hiding/inert/focus handling; opacity alone does not prevent interaction. For popovers use built-in provider primitives to manage focus/dismiss.

## Easing and durations

Choose direction by perceived physics: an entering panel generally decelerates into place; dismissals should feel responsive and not hold the user hostage. Use the project's motion tokens first; e.g. --motion-fast 120–200ms for simple state and a somewhat longer panel travel only if justified. These are *starting ranges*, not fixed truth. Spring parameters must come from measured/reviewed recipes compatible with installed library and interruption expectations.

## WAAPI example: interrupt safely

~~~js
const animation = element.animate(
  [{ opacity: 0, transform: 'translateY(6px)' },
   { opacity: 1, transform: 'translateY(0)' }],
  { duration: 170, easing: 'ease-out', fill: 'both' }
);
animation.finished.catch(() => {
  // Cancellation is expected during route change or new interaction.
});
~~~

Cancel/reverse prior instances and clean up on unmount; don't leave fill-modes masking final CSS state. An animation is not a promise of successful network work. Test click during exit and rapid alternating toggles.

Official API reference: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API and source inspiration https://github.com/emilkowalski/skills/blob/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/animate/SKILL.md .
