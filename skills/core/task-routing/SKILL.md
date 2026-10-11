---
name: task-routing
domain: core
version: "0.1.0"
description: >-
  Use when a new software engineering request arrives and it is unclear which workflow or skill is warranted. Do not use to force a heavyweight process onto tiny edits.
---

# task-routing

## Decision
Classify the change by blast radius, ambiguity and reversibility. Choose LIGHT for localized edits; STANDARD for a normal feature touching several files; DEEP for authentication, sensitive data, production, architecture or migrations. Use the least expensive mode compatible with risk.

## Skill selection
Start with no more than two narrow skills. Match the user intent against descriptions, including negative triggers. Load skill bodies only when relevant; read references only to answer a current need. Never recursively ingest the skill tree.

## Execution
For LIGHT, implement directly and verify. For STANDARD, write acceptance criteria then implement and test. For DEEP, plan rollback, trust boundaries and independent review. Do not invent subagents, budgets or test evidence. Escalate only when the current task provides a reason.

## Done when
You can explain why this workflow was selected, what changed and which checks actually ran.
