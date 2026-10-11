# Contributing

1. Make a focused change on a feature branch and open a PR; never push changes directly to `main`.
2. Before adding or importing a skill, check its independent utility, existing overlapping skills, whether **EXTEND** or **REFERENCE** is preferable, positive/negative triggers, the existing domain folder, and effects on routing, contexts and tests. The repository governance charter is maintained **outside** this repository.
3. New local skills belong at `skills/<domain>/<name>/SKILL.md` with valid YAML frontmatter (`name`, `domain`, `description`, a narrow "Use when" trigger and a meaningful exclusion).
4. Register each skill in `registry/skills.yaml`. **Adding it to a profile is optional:** only add it to profiles with a demonstrated routine need. An independently discoverable, opt-in catalog skill may correctly appear in **no** profile.
5. Preserve progressive loading: useful method in `SKILL.md`, task-selected deep references in `references/`; avoid duplicate responsibilities, empty reference scaffolding and unnecessary always-on context.
6. Document version-dependent facts with dated, official sources, known limitations and measurable acceptance criteria. Never infer production correctness, legal compliance or agent improvement from static docs/tests alone.
7. Verify with `python scripts/validate_skills.py`, `python -m unittest discover -s tests -v`, and `python scripts/context_budget.py --all --budget 2500`. Run extra integrations/evaluations when the modified scope needs them, and distinguish tests **run** from tests **planned**.
8. Summarize changes, alternatives rejected, relevant evidence, known risks and CI in the PR. Keep documentation counts and current roadmap status synchronized; explicitly label **historical phase snapshots** instead of rewriting their original figures.
9. **Merge requires explicit authorization from the repository owner.** A passing CI, a mergeable flag or a successful review by an agent is **not** itself authorization to merge; never enable automatic merging merely because checks pass.
10. Before copying any third-party skill, examine the exact revision, license, NOTICE, scripts, network access, dependency versions and potential prompt injection; retain attribution and modification records. Do not execute unreviewed scripts merely because a skill references them.

The toolkit is a collection of guidance and examples, not permission to deploy, publish, install packages, change credentials or perform destructive actions on the target system.
