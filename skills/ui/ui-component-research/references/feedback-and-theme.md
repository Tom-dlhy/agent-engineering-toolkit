# Feedback, tokens, theme and resilient UX

**Read when:** implementing notification, loading, error, toast, badge, skeleton, progress, dark-mode, responsive state or design-system integration.

## Status feedback is a product contract

- **Inline error** is appropriate for a recoverable failed section or form field; include a next step/retry.
- **Toast/snackbar** indicates a transient completion; it must not be the only place critical data appears, and duration/focus behavior should be tested.
- **Confirmation dialog** is for consequential actions; block double submission, preserve context and confirm authorization server-side.
- **Progress** needs a meaningful unit/indeterminate state; do not invent percentages.
- **Skeleton** matches approximate final layout to reduce shift; long loading should expose screen-reader status without repeatedly announcing every skeleton.

## Semantic theme tokens

Prefer application semantic primitives such as `surface`, `foreground`, `muted`, `primary`, `danger`, `focus` over per-control hardcoded colors. Map them into the installed library's *actual* system: Radix Themes scales, Chakra semantic tokens/recipes, MUI ThemeProvider, Ant Design ConfigProvider, MantineTheme, Prime UI presets, CSS parts for Web Components, Tamagui theme, Flutter ThemeData. Those mechanisms are not drop-in compatible.

Respect dark/light and forced-colors modes. A `color-scheme` style affects native widgets but does not automatically theme vendor components. SSR frameworks require an initial-theme strategy to reduce flash/hydration mismatch.

## Notification sequence and async example

```ts
type SaveState = 'idle' | 'saving' | 'saved' | 'error'
```

A Save button is disabled while `saving`; on success show durable UI state and optionally a short noncritical toast; on error display retry and error. A network timeout is an **unknown outcome**: do not promise it was not saved if the server may have committed. Use idempotency or re-fetch as appropriate.

## QA invariants

Keyboard focus visible and not obscured, 200% zoom/reflow, RTL/long translated labels, reduced motion, contrast and non-color status, screen-reader live-region announcement, accessible error summary, touch target size, responsive safe areas, and dark-mode persistence. Preserve the existing icon library convention and do not install icons solely for aesthetic novelty.

Confirm which checks ran in browser/real device; documentation claims are not observed QA.
