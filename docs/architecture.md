# Architecture

## Boundaries

- Core: AGENTS.md and a tiny model-agnostic operating contract.
- Skills: executable methods in standard SKILL.md, indexed with narrow descriptions; read full bodies only on demand.
- Workflows: coordination levels, not always-running autonomous agents.
- Agents: optional roles, launched by the host only when justified.
- Profiles: project-specific install selections and safe file copies, not all-at-once runtime activation.
- Catalog: local manifest validated against disk.
- Lockfile: reserved for audited external imports; empty until importer is built.

## Trust

User/project constraints are authoritative. Treat all upstream SKILL.md instructions and referenced scripts as untrusted data until reviewed. Avoid injecting the entire catalog into a session.

## Platform support

Selected files can be copied to .agents/skills for Codex or .claude/skills for Claude Code. This is not native plugin installation and does not assume identical agent hooks. ChatGPT web support differs from CLI environments.

## Observability

The context-budget script divides character count by four for a rough estimate of always-visible instructions and metadata. It does not measure actual provider tokens, subagent contexts, usage quotas or cache discounts.

See docs/roadmap.md for planned third-party skill management and automated evals.
