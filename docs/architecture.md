# Toolkit architecture

## Progressive disclosure

The local catalog has 113 skills across 12 domains. Seven AWS cloud skills retain expert-v2, the 35 UI providers and 11 design/growth/intake skills retain expanded-v2, and 13 Python/LLM/cloud skills now use expanded-v2 deep references. Other technical skills remain under review.

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

## Expertise maturity (phase 1)

Original 59 skills had no reference leaves. Phase 1 introduces 14 AWS leaves; the reconciled UI work adds 70 provider-specific leaves, 4 component-family leaves and a library-selection index, all read on demand. Skills marked `maturity: expert-v2` or `maturity: expanded-v2` in the registry are structurally gated; this flag is **not** proof of production correctness. See [expertise audit](expertise-audit.md) and [progressive skill contract](progressive-expertise.md). Never treat pending technical skills as complete simply because they are registered.
