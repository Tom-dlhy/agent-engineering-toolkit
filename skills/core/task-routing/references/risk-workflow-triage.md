# Risk-first workflow selection and escalation

**Read when:** deciding whether a change needs LIGHT, STANDARD or DEEP workflow,
especially when impact, permissions or reversibility are ambiguous.

## Work from the concrete diff, not the word list

A request mentioning a database can be a harmless documentation edit; a seemingly simple
change to a password reset token is security-sensitive. First identify what can actually
change in the system, who may be affected, whether data/state crosses a trust boundary,
what rollback means and which tools are authorized.

| Signal | LIGHT | STANDARD | DEEP |
|---|---|---|---|
| Scope | Known local reversible change | One feature across files/interfaces | Contracts across services, shared state or infra |
| Uncertainty | Reproduction or desired edit clear | Some requirements/design choices | Major unknowns or unverified invariants |
| Side effects | No external mutation | Controlled internal writes | Production deploy/data/security/irreversible effects |
| Proof | Focused check + diff | Unit/integration + review | Rollback rehearsal, security/negative tests, staged validation |
| Coordination | One implementer | Plan and owner | Explicit risk plan; independent review when valuable |

Use the smallest mode that preserves guarantees. A DEEP decision does not make subagents
mandatory, and a LIGHT decision does not waive security boundaries.

## Escalation and de-escalation protocol

1. Classify initial risk and state what evidence supports it.
2. Check permissions before privileged/destructive actions. A proposed command is not
   authorization to run it.
3. When a failing test reveals broader impact, re-evaluate touched contracts rather than
   silently changing many unrelated files.
4. When isolated evidence disproves the broad failure theory, reduce investigative scope
   and avoid costly orchestration.
5. Prefer small reversible commits, explicit rollback/compensation, and a decision log
   for irreversible operations.
6. Preserve existing constraints and project approvals. A task may be implementable
   without permission to deploy or merge.

## Worked triage

"Update the SQL migration README" is LIGHT if no migration code or runtime changes.
"Run a migration that drops a production column" is DEEP even if the command is short:
validate backup/recovery, affected consumers, staged dry-run and user authorization.
"Investigate intermittent 503" starts with systematic-debugging; its risk increases only
when evidence shows production effect or the proposed fix alters deployment/runtime.

## Common failures

- Treat lexical `production` as permission to access production.
- Mark a task DEEP merely because the repository is large.
- Continue a LIGHT hotfix after discovering changed auth/tenant invariants.
- Spend more time preparing a plan than executing a fully specified local fix.
- Confuse mode with required reference depth.

## Final record

Mode, scope, known risks, evidence for escalation, checks, remaining uncertainty and
whether any action requires separate approval. This is a methodological decision aid,
not a compliance certification.
