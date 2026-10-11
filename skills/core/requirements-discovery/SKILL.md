---
name: requirements-discovery
domain: core
version: "2.1.0"
description: >-
  Use when explicitly asked to clarify, pressure-test or scope an ambiguous
  idea, feature or software specification, or when one truly blocking business
  decision prevents safe implementation. Do not interrogate the user for
  adequately specified edits or repeat information already supplied.
---

# Requirements discovery — high-information questions, minimal friction

## Purpose and entry rule

A user may explicitly ask for /grill-me or clarification, but an ordinary
implementation request is not automatic permission to delay work with a
questionnaire. First inspect the full brief/repo context. Distinguish user
facts, reasoned assumptions, open decisions and explicitly excluded scope.

## Decision process

1. Identify intended user/job, trigger and observable outcome; record already
   specified constraints before deciding if anything is missing.
2. Classify unknowns by **decision impact × irreversibility**. If safe
   reversible assumptions suffice, state them and implement; otherwise ask
   the smallest blocking question, one at a time unless the user prefers a batch.
3. For requested discovery, pressure-test real use cases and failures:
   authorization, duplicate/partial input, timing, cost, privacy, scaling,
   data retention, human approval and manual recovery where relevant.
4. Convert answers into scope/non-goals, acceptance scenarios including
   at least one meaningful negative path, stakeholders/deciders, outstanding
   decisions and testable success measures.
5. Stop when additional questions have little effect on the next decision.
   Hand off to `architecture-decision` for technology choices or task-routing
   for implementation workflow. Do not invent agreement or silently approve
   irreversible choices.

## Examples

| Task | Behavior |
|---|---|
| User says "fix typo in header" | Implement directly; don't ask for personas |
| User says "grill my SaaS idea" | Focused interview about users, workflow, willingness to pay and risks |
| User requests auto-send email but review policy unknown | Ask whether sending is authorized or draft safely |
| Ticket triage workflow | Clarify classification suggestion vs state-changing autonomous action |

## References

- [Question priority and problem framing](references/problem-framing.md) —
  **read when** user intent, actors, constraints or business scope are uncertain.
- [Acceptance scenarios and decision log](references/acceptance-and-decision-log.md) —
  **read when** producing a testable specification or review handoff.

## Exit

Confirmed facts vs assumptions, measurable outcome, normal/error paths,
non-goals, decisions needing approval, and only questions that genuinely
block progress. Respect user's preference for direct implementation and
avoid adversarial or patronizing questioning.
