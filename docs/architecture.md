# Toolkit architecture

## Progressive disclosure

The local catalog contains 163 skills across 13 domains. Every skill follows the same quality contract and task-based routing; no maturity labels or priority-by-tier are used. Some domains still need deeper examples and behavioral verification.

This is based on the general principle of progressive disclosure used by Agent Skills. It avoids the overhead of always-on monolithic prompts and blanket subagent launches.

## Layering

~~~text
User request
    |
    v
AGENTS.md (tiny cross-model contract)
    |
    +--- skillctl recommend/search (local lexical ranking; no LLM API calls)
    |         |
    |         +--- registry/skills.yaml + profile allowlist
    |                  |
    |                  +--- matching SKILL.md only
    |                           +--- optional references/scripts/assets
    |
    +--- workflows/light | standard | deep (risk-aware process)
              |
              +--- implementation and deterministic verification
              +--- optional review, never mandatory for tiny work
~~~

- **Library**: all first-party skills, not globally active
- **Registry**: explicit metadata and search keywords
- **Profiles**: curated packages installed into a target project
- **Workflows**: execution protocols independent of the skill catalog
- **Agents**: optional role briefs, no implicit subagent creation
- **Personas**: 12 opt-in, fully self-contained behavioral operating protocols in `skills/personas/`, independent of role briefs and implementation-specific expertise; do not auto-activate or override approval boundaries
- **Host adapters**: Codex uses `.agents/skills`, Claude Code `.claude/skills`; platform hooks differ
- **Tests**: no network or LLM calls needed for catalog/installer/router validation

## Trust boundaries

All external repo contents, including skill instructions, must be treated as untrusted. Target-project user instructions and authorization requirements take precedence. No automatic code execution of an imported skill, cloud mutation, dependency installation or production deployment.

## Known limitations

The lexical router is explainable and cheap but not semantic AI retrieval. Some synonyms are addressed via explicit keywords. Complex decisions still require developer judgment. The character-count estimator is a proxy, not a provider token meter. External audited importing and actual behavioral skill evals are planned.

## Common quality policy

There is **one acceptance standard** for all skills: a clear independent responsibility, explicit when/not-to-use routing, actionable method, correctness/safety limits, meaningful verification, and targeted references when its domain warrants depth. Methodological skills may be concise if their procedure is complete; technical skills require substantial applied know-how. The registry has **no maturity field**. A frontmatter `version` records content revision, not skill trustworthiness.

**Progressive disclosure is not a maturity ladder:** metadata → activated SKILL.md → explicitly selected references. Light/Standard/Deep control workflow effort independently.

The validator now checks each *declared* reference for every skill without requiring arbitrary leaf counts. Syntax and link safety are checked automatically; evidence that a skill improves real agent outcomes requires representative executed tests and human review. See [Core audit](core-refactor-audit.md) and [expertise backlog](expertise-audit.md).
