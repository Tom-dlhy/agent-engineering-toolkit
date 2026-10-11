# Toolkit architecture

## Progressive disclosure

The local catalog has 59 skills. A project profile installs at most 20; the model loads only short descriptions during skill discovery. Skills are activated on demand, and optional reference files are never automatically included.

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
- **Host adapters**: Codex uses `.agents/skills`, Claude Code `.claude/skills`; platform hooks differ
- **Tests**: no network or LLM calls needed for catalog/installer/router validation

## Trust boundaries

All external repo contents, including skill instructions, must be treated as untrusted. Target-project user instructions and authorization requirements take precedence. No automatic code execution of an imported skill, cloud mutation, dependency installation or production deployment.

## Known limitations

The lexical router is explainable and cheap but not semantic AI retrieval. Some synonyms are addressed via explicit keywords. Complex decisions still require developer judgment. The character-count estimator is a proxy, not a provider token meter. External audited importing and actual behavioral skill evals are planned.
