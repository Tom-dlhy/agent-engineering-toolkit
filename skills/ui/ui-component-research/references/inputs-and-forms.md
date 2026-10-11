# Input, form and selection engineering

**Read when:** an input, validation form, combobox, autocomplete, multi-select or date picker is being implemented or reviewed. Not needed for a visual-only button change.

## Decide state ownership before markup

Choose *one* form state authority: HTML + browser validation, a framework form library, or provider-managed form controls. The app can mirror state for rendering, but must avoid a second competing source of truth. Inspect component prop contract and type of submitted value; React Aria collections, MUI Autocomplete option objects, Angular Reactive Forms and Flutter FormField do not expose interchangeable semantics.

| Requirement | Correct mechanism | Common failure |
|---|---|---|
| Label/hint/error | Native label or provider Field/FormItem, linked `aria-describedby` and status | Placeholder as the only label; error not announced |
| Required vs disabled | Distinguish HTML `required`, schema/business validation and `disabled` (often omitted from form submission) | Treating disabled as read-only or a server authorization |
| Controlled values | Choose clear value/selectedKeys/inputValue ownership | Selected option reset when a new list object arrives |
| Async options | Debounce, abort/stale-response guard, busy/empty/error | Old search response overwrites newer options |
| Multi-select | Stable option keys, keyboard remove, accessible chip names | Array indices as identity |
| Date/time | Local date vs UTC instant, locale/calendar/timezone decisions | Off-by-one day after serialization |

## Basic accessible React example (provider-agnostic HTML)

```tsx
import { useId, useState } from 'react'

export function EmailField() {
  const id = useId()
  const [email, setEmail] = useState('')
  const valid = email === '' || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)
  return <div>
    <label htmlFor={id}>Email</label>
    <input id={id} type="email" value={email}
      onChange={e => setEmail(e.currentTarget.value)}
      aria-invalid={!valid} aria-describedby={!valid ? id + '-error' : undefined} />
    {!valid && <p id={id + '-error'} role="alert">Enter an email address</p>}
  </div>
}
```

This regex is illustrative UI feedback, **not** a reliable email verification or a substitute for server validation. A provider's Field or form library should be used instead of copying HTML if it supplies the equivalent accessible contract.

## Test scenarios

Submit valid/invalid, keyboard Enter, Tab/Shift+Tab, disabled/read-only, autofill and IME, selected item after async refetch, no results, screen reader error announcement, focus after reset, locale change and server error rehydration. Check actual package's documented form and collection APIs. Do not claim a provider is accessible solely because a component renders.
