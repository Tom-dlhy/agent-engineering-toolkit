# Skill discovery, collision handling and progressive context

**Read when:** more than one skill plausibly matches a task, an installed profile
lacks a capability, or the route/activation cost must be examined.

## Four different states

1. **Cataloged:** registry contains name/path/description/keywords.
2. **Installed:** a specific agent host/profile actually exposes the skill.
3. **Activated/read:** the agent has loaded the SKILL.md of a relevant skill.
4. **Reference accessed:** the agent has read an explicitly selected leaf for the current task.

None implies the next. A CLI search score is deterministic token overlap, not semantic
certainty, behavioral evidence or authorization.

## Resolution algorithm

Given a task such as "FastAPI returns 422 when patching a resource":

- Choose `systematic-debugging` if the failure is unexplained, and `fastapi-service`
  for endpoint/Pydantic contracts. Do not pull in `python-persistence` unless DB write
  semantics are involved.
- For "create a new core skill about reviewing tests", inspect `skill-authoring`,
  `verification-before-done` and `quality/test-strategy`. Prefer REUSE/EXTEND/REFERENCE;
  add a separate skill only if the task intent and trigger are independent.
- For "choose a UI library", select `ui-library-selection`, then **one** library
  specialist if chosen; not all 35 vendor skills.

## Search and explicit read

~~~bash
python scripts/skillctl.py search "FastAPI validation 422" --profile python-backend
python scripts/skillctl.py show fastapi-service
python scripts/skillctl.py references fastapi-service
python scripts/skillctl.py read-ref fastapi-service references/schemas-and-errors.md
python scripts/context_budget.py --profile python-backend --activated fastapi-service
~~~

The CLI does not invoke skills natively in Codex/Claude; the host must actually load them.
Commands are examples to run only in a checkout with the expected scripts. The budget
uses **characters/4** as a rough estimate, not real provider billing tokens.

## Collision and negative triggers

Inspect name, keyword score, explicit exclusions and available project context. A high
lexical score may be wrong when a name shares "review", "testing" or "architecture".
If no confident match exists, choose manually or use no specialist rather than fabricate
confidence. Do not install a third-party skill because its name resembles a user request.

## Testing router changes

For every changed core keyword/description, test a positive query, a close negative
candidate, an ambiguous query and an unmatched query. Check installed-profile constraints,
missing references, symlink/path traversal and effect on discovery budgets. Avoid adding
generic high-frequency words (e.g. "code", "test", "feature") to every skill.

## Exit

Report the selected skill(s), why near-duplicates were excluded, whether each was installed
and actually read, and any unmeasured activation/token behavior.
