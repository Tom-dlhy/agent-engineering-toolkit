# Motion runtime — interruption, performance and accessibility

**Read when:** animations jank, don't cancel correctly, break keyboard/focus interaction or trigger accessibility complaints.

## Interruption matrix

| Event | Required behavior |
|---|---|
| Open → immediately close | Reverse/cancel coherently; no stale animation completion reopening |
| Route unmount during transition | Cancel pending animation; restore/transfer focus safely |
| Async task finishes during exit | Do not resurrect unmounted UI or announce success twice |
| User presses reduced motion toggle | Remove movement while preserving visible feedback |
| Background tab or low-end CPU | Motion may be skipped; content/state must remain correct |
| Modal + nested dropdown | Let provider control focus/stack, not duplicated homemade loops |

Do not conflate animation completion with business transaction completion. State model should be authoritative; animation expresses state, never secretly owns it.

## Profiling method

Record a repeatable interaction on representative low-end device or throttled browser. Use DevTools performance timeline or runtime instrumentation: long tasks, layout/paint cost, compositing layers, memory and dropped frames. Isolate expensive filters, oversized repaints, JS per-frame work and repeated measurements. Avoid optimizing from the visual appearance of a single desktop screenshot.

### Scroll and gesture concerns
Scroll-linked effects can use platform capabilities when supported, but beware accessibility, nested scroll contexts, gesture cancellation and overscroll. Movement tied to pointer movement must not interfere with selecting or reading content. Use passive listeners only when appropriate; do not disable scrolling indiscriminately.

## Reduced motion strategy

~~~css
@media (prefers-reduced-motion: reduce) {
  .decorative-float { animation: none !important; }
  .route-transition { transition-duration: 0.01ms; }
}
~~~

This preserves state feedback via text, opacity or immediate visibility. Some users tolerate subtle opacity but not spatial travel—prefer capability to disable nonessential movement entirely.

## Accessibility QA

Confirm content accessible before/after, controls remain actionable with keyboard, focus returns after modal close and status announcements aren't delayed until a nonessential exit finishes. Check contrast during fades and that active controls never briefly become invisible yet focusable.

## Evidence

Record actual device/browser, reduced-motion setting, trace findings and before/after measurable impact. Don't claim 60fps without measurement.

Primary references: https://web.dev/articles/animations-guide and https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion . Method inspiration: https://github.com/emilkowalski/skills/blob/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/review-animations/SKILL.md .
