# Accessible forms, dialogs and dynamic status

Read when: building or correcting form validation, dialog behavior, interactive composites, dynamic announcements or keyboard recovery.

## Forms: link input, label and repair instruction
Prefer native HTML labels, input types and browser-valid constraints. Bind validation messages to the corresponding field with `aria-describedby` when custom inline help/errors exist; use `aria-invalid="true"` when an error has been detected, not merely because the field is required. Present a focused error summary for multi-field failures when needed. Don't replace semantic labels with placeholder-only text.

```html
<label for="email">Email address</label>
<input id="email" name="email" type="email"
       autocomplete="email" aria-invalid="true"
       aria-describedby="email-error" required />
<p id="email-error">Enter a valid email address.</p>
```
The snippet illustrates an invalid **post-validation** state. In normal state remove `aria-invalid` and error reference as appropriate. Backend must still validate input, and generic status messages must not leak sensitive data.

## Dialog contract
Prefer a mature accessible component from the installed UI provider. Check documented behavior rather than bolting on conflicting custom traps:
1. Trigger has a meaningful accessible name and opens dialog.
2. Dialog has a visible or programmatic accessible name; describe only useful supporting context.
3. On open, focus moves to a meaningful item. Tab/Shift+Tab stay within a modal. Escape closes if closure is allowed.
4. On close, focus returns to the trigger or a logical successor when the trigger is removed.
5. Background is genuinely inert for modal use; hidden content isn't merely transparent but keyboard-focusable.
6. Long content scrolls without placing essential close/actions outside reachable area.

Dynamic results: use a restrained role=status/live region for nonurgent outcomes; use alert only for critical interruptions. Announce errors and changes once, not on each keystroke. Use native button to submit, never a clickable div with manually recreated semantics.

## Negative and manual checks
- Open -> Tab cycle -> Escape -> return focus; test nested or destructive confirmation appropriately.
- Validation via empty submit, malformed email, submit after correction; labels and errors read by representative screen reader.
- Loading -> success/error: no focus loss, hidden content isn't announced, retry path reachable.
- Form zoomed to 200%/400%, translated text and mobile virtual keyboard open.
- Never infer VoiceOver/NVDA results from the DOM alone.

Official: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ and https://www.w3.org/WAI/tutorials/forms/notifications/
