# AET A/B/C benchmark suites

Suites are **vetted executable fixtures**, not natural-language eval scenarios.
The host evaluation is intentionally opt-in and must run in a **separate
disposable computer/container/VM**. Native CLIs can see user configuration,
credentials and network; a Python temporary directory is NOT isolation.

Each JSON suite has 1..30 tasks with the following fields:

- id: unique kebab-case task identifier.
- prompt: identical literal user task across the three arms.
- fixture_dir: relative path under the AET source checkout.
- fixture_sha256: pinned content digest from plan output (required for run).
- technical_skills: explicit names, maximum 5, for the knowledge-only arm.
- check_argv: **trusted argv array**, never shell text; run separately after
  model completion. It may execute arbitrary fixture code.
- expected: independently determined observable success criterion.
- risk: light/standard/deep. Risk is descriptive; no skipped approval gate.

Use the quick-start example as an illustrative source only. It deliberately
has fixture_sha256 null; run "plan" to compute its digest, review fixture
contents and copy digest into your own committed suite. Do not spend credits
or run unknown checks without reviewing them.

For serious results include: diverse already-green baseline tasks, negative
authorization/replay cases, routine bug fixes and complex API integrations.
Separate tasks used during skill editing from held-out evaluation tasks.
Do not grade acceptance based on an agent's answer alone. A human reviewer
must assess actual diff, unintended files and high-risk test coverage.

Record actual activation separately from skill installation. The default
runner records mounted_skills but sets observed_skill_activation to null:
native log correlation has not yet been implemented and **availability
does not establish skill use**. Token counts are null when the host does
not expose known structured usage fields.

Historical evals/*.yaml describe scenarios and are NOT native-run datasets.
