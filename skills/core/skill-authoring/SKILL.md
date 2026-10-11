---
name: skill-authoring
domain: core
version: "0.1.0"
description: >-
  Use when creating, modifying or splitting an Agent Skill for the toolkit. Do not use for normal code editing that does not affect skill behavior.
---

# skill-authoring

## Authoring contract
A skill is a task-specific method, not a generic instruction to act like an expert. Create skills/<domain>/<name>/SKILL.md with YAML frontmatter fields name, description and domain. The description is a routing interface: say explicitly when to use the skill, and when not to use it.

## Keep it lightweight
Keep body concise and actionable: prerequisites, procedure, verification, failure modes. Put large provider reference material in optional references instead of permanent instructions. Prefer deterministic scripts over prose for machine-verifiable checks.

## Validation
Register the skill and edit only relevant profiles. Run the repository validator and tests. Evaluate on at least one positive trigger, one negative trigger and one ambiguous case. Record upstream attribution before adapting third-party content.

## Never
Never demand skill invocation for every task, copy licensing blindly, or execute an unreviewed installer.
