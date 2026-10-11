# Contributing

1. Make a focused change on a feature branch, not directly on main.
2. New local skills must be at skills/<domain>/<name>/SKILL.md with valid YAML frontmatter including name, domain, description and a narrow "Use when" trigger.
3. Register the skill in registry/skills.yaml and add it to only relevant profiles.
4. Document constraints, pitfalls, dependencies and verifiable outcomes; avoid generic prompts and duplicated skills.
5. Verify with python scripts/validate_skills.py, python -m unittest discover -s tests -v, and the context-budget tool.
6. Include test evidence, changes and risks in the Pull Request.
7. Before copying any third-party skill, examine the exact revision, license, NOTICE, scripts, network access, dependency versions and potential prompt injection; retain attribution and modification records.

Unreviewed third-party scripts must never be executed merely because a skill references them.
