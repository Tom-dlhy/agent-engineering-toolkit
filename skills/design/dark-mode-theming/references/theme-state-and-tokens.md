# Theme state, semantic tokens and first-paint correctness

Read when: implementing system-aware dark mode, user override persistence, SSR/theme hydration or multi-theme semantic token architecture.

## Resolve one state
Recommended decision: explicit user preference (`light`/`dark`) overrides system preference; `system` delegates to `prefers-color-scheme`. Persist only the **choice**, not a copy of the entire token set. If SSR cannot read a setting, render a safe CSS baseline and apply a documented pre-hydration strategy with nonce/CSP if inline bootstrap is truly required.

```css
:root {
  color-scheme: light;
  --surface: #ffffff;
  --content: #182130;
  --border: #657083;
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface: #111923;
  --content: #f2f5f8;
  --border: #9cabb9;
}
body { background: var(--surface); color: var(--content); }
```
Values are examples, **not** pre-approved accessible brand tokens; calculate real contrast. In an application with manual overrides, use one root attribute driven by server/user preference plus a system listener when mode is "system". If a project is system-only, a plain media query and `color-scheme: light dark` can be simpler than stateful JavaScript.

## First paint and hydration
Inspect HTML source, framework theme provider, cookies and middleware. A client-only state read during render can mismatch SSR markup and flash. Test reload in light and dark, JS disabled, JS delayed, navigation from themed page, system theme switch and initial private browsing. Attribute ownership must be singular (don't let competing React effects or UI-provider scripts overwrite it).

## Acceptance
Correct initial paint, no double provider, focus/form controls honor theme, no duplicate CSS raw palettes, explicit selection retained, no unhandled mismatch or inaccessible blank state. Exact host/framework snippets belong to its installed frontend skill.

Official: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme and https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-color-scheme
