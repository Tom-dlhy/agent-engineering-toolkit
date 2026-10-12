# Review focus, falsifiable risks and negative acceptance

**Read when:** a planned change crosses security, persistence, concurrency, public interfaces, production operations or a high-uncertainty dependency.

## Turn speculative risk into an observable scenario

Review Focus is the set of relevant failure classes **not already
adequately exercised by task tests**. List the highest-impact risks, not
a catalogue of every possible bug. Each entry names input or condition,
the invariant, likely consequence, and the check or reviewer question.
The spec may omit hostile inputs; it does not authorize insecure defaults.

Examples:
- Cross-tenant document ID: another tenant gets denial and zero write/read,
  not a 200 with an empty result that leaks metadata elsewhere.
- Retry after remote timeout: operation ID prevents a duplicate payment or
  duplicate dispatch; timeout is not proof nothing happened.
- Source changes during migration: partial rollout preserves old and new
  reader compatibility; rollback does not assume schema drops are reversible.
- Missing configuration: no silent production fallback to development key.
- Concurrent branch integration: task-level tests may pass separately,
  while the merged result breaks a shared import; test the combined tree.

## Select review level by evidence

R0: self-review and focused checks when a localized reversible edit has
a reliable oracle. R1: a scoped independent review when a public contract,
coupled files, uncertainty or ordinary multi-component complexity justifies
fresh context. R2: a risk-led independent review for sensitive data,
authorization, irreversible effects, migration or high-impact failures;
add spec compliance plus code quality/security gates where required.
Review level is not merely the workflow name, and an unavailable independent
reviewer must be reported as an unmet gate rather than fabricated.

Avoid double-reviewing an identical unchanged diff. Review packages contain
spec, BASE..HEAD, actual check outputs, sensitive trust boundaries,
non-goals and specific uncovered risks. Change a finding's severity only
after considering user impact, not merely whether an ambiguous requirement
mentioned it explicitly.

## Risk matrix and stopping rule

Evaluate (impact if wrong) × (exposure / likelihood) × (ability to detect and
recover). A single high-consequence risk can dominate many benign files.
Reversible cosmetic work with immediate feedback does not merit a second
model. A one-line permissions bypass does.

If a risk cannot be addressed without an owner decision, capture a precise
blocker and stop that action. Do not turn every uncertainty into an interview:
record a safe default for reversible choices. Track untested limitations as
BLOCKED or NOT RUN, never PASS.

## Example review package focus

Feature: tenant uploads. Risk focus: path traversal, symlink races,
cross-tenant lookup, oversized file, partial upload cleanup and replayed
requests. Include exact branch SHA, minimal reproducer, affected public
contracts, tested environments and tests skipped. A reviewer should be able
to discover a fault without reading the implementer's chat history.
