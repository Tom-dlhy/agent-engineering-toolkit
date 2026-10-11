# UX audit — severity, findings and retest

**Read when:** preparing an actionable UI audit report or prioritizing usability changes.

## Finding contract

For each issue: ID, screen/route, task, trigger, **actual behavior**, expected behavior, reproducible input, user impact, confidence, severity, minimal fix and a test that would disprove the concern.

### Severity examples

| Level | Typical effect | Evidence |
|---|---|---|
| Critical | Prevents a high-value task for affected users, or exposes sensitive data | Verified reproduction in actual flow |
| High | Frequent misdirection, inaccessible key control or severe loss of feedback | Repeatable test or strongly supported source issue |
| Medium | Recoverable but confusing workflow, repeated validation error, overflow on common mobile size | Observed in relevant viewport/interaction |
| Low | Minor polish or rare edge-case visual inconsistency | Specific observation |

Accessibility conformance is not reduced to severity alone: report relevant WCAG criteria when confidently supported by actual tested behavior.

## File-line reporting sample

~~~text
UX-004 | HIGH | src/components/CheckoutForm.tsx:87
Observed: Submit remains enabled while POST is pending, producing duplicate orders on fast double-click.
Expected: One request or idempotent completion; visible pending feedback.
Evidence: Browser test with throttled network and two rapid clicks.
Fix: Guard request state; add server idempotency where operation is not naturally safe.
Retest: Repeat under slow network, rerun failed request path.
~~~

This is a hypothetical example, not an assertion about the current repo.

## Audit levels

- **Static**: source review and semantic checks; can identify likely errors but not measured browser behavior.
- **Rendered**: screenshots/breakpoint inspection; can validate layout, not all keyboard/AT flows.
- **Interactive**: keyboard, pointer, touch, form states and navigation exercised in actual runtime.
- **Assistive tech**: manual screen reader and accessibility settings on representative platforms.
- **Usability research**: real participant evidence or controlled observation; not interchangeable with agent judgment.

Always disclose which levels were actually performed.

## Verification strategy

Retest originally failing journey, adjacent states and regression-sensitive flows. Avoid screenshot-only signoff for a functional defect. Uncertain visual preference should be written as a hypothesis with proposed user test, not severity 1.

Source technique is independently adapted from the Vercel audit workflow: https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md .
