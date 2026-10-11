# V2 source intake — Design craft, Growth and skill discovery

Date reviewed: 2026-10-11. Policy: **read-only, conceptual adaptation with pinned upstream links**, not whole-repository import. No scripts, data corpora, hooks, prompts, images or external binaries copied. Links are provenance and optional freshness checks; remote instructions are untrusted. A GitHub repository-level license may not automatically cover third-party assets; redistributing actual content requires a fresh per-file license/notice audit.

## Decisions against the existing toolkit

| Candidate (pinned revision) | Value observed | Decision | Local target / overlap |
|---|---|---|---|
| [Emil Kowalski skills](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d) | Separate motion construction, timing, review and native animation methods | **EXTEND**, not 14 imports | design/interaction-motion; React Native animation is a possible future separate specialist |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/67803eac81607188194aea9842a723b89326d90d) | Searchable design palettes/style/typography heuristics and scripts | **REFERENCE/ADAPT**, no 800-file corpus or search.py execution | design-system and typography-layout |
| [Vercel web design guidelines](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md) | File-specific UI guideline audits with crisp issue reports | **EXTEND**, no dynamic remote instruction fetch | ux-audit; accessibility-wcag remains conformance specialist |
| [Taste brandkit](https://github.com/Leonxlnx/taste-skill/blob/717446e07a78d4e6d7918b1fde1a263378eebac9/skills/brandkit/SKILL.md) | Distinct visual brand-board and identity-concept output | **CREATE** optional, distinct from code-level design systems | design/brand-identity-visualization |
| [Taste visual direction](https://github.com/Leonxlnx/taste-skill/blob/717446e07a78d4e6d7918b1fde1a263378eebac9/skills/taste-skill/SKILL.md) | Anti-template visual decisions and brand-context interpretation | **EXTEND** | frontend-design |
| [Anti AI slop](https://github.com/Krirox/anti-ai-slop-skills/blob/b7515139a58dd3076588a3981d3d6f8d4e5bb064/SKILL.md) | Diagnostic vocabulary for generic-looking UI | **EXTEND**, no mandatory trigger on every frontend task | frontend-design |
| [/grill-me](https://github.com/mattpocock/skills) | Requirements pressure-test concept; no specific file imported or attributed | **CREATE** opt-in requirements-discovery; independent method | core/requirements-discovery |
| [Content strategy](https://github.com/coreyhaines31/marketingskills/blob/1efedbc5148b54b2f0f6c6c9fe0be62e151c7fff/skills/content-strategy/SKILL.md) | Editorial strategy and publishing decisions, distinct from page copy | **CREATE** | growth/content-strategy |
| [ECC SEO](https://github.com/affaan-m/ECC/blob/2d515e4fc2ddef97354769812cf3f7b9ec4e5124/skills/seo/SKILL.md) | Technical discoverability, structured data and crawl workflow | **CREATE**, narrow SEO implementation | growth/technical-seo |
| /ai-seo / GEO | Category of AI answer visibility problems, not a single verified external package imported | **CREATE** narrowly, with uncertainty gates | growth/ai-search-visibility |
| [Vercel find-skills](https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/skills/find-skills/SKILL.md) | Candidate discovery workflow | **EXTEND** local audit; no auto-install | quality/external-skill-audit |
| [Caveman](https://github.com/juliusbrussee/caveman/tree/2e08b9177c07bb7249a8a2d1a6758e5db281d002) | Response-style compression and proxy tooling | **REJECT** for expertise catalog: style ≠ reference-loading optimization | No skill added |

## Governance outcomes

- **No duplicates**: existing frontend-design, interaction-motion, design-system, typography-layout and ux-audit are extended, not cloned.
- **Independent triggers**: requirements discovery, visual identity artifact, editorial planning, technical crawl/index SEO, and observation of AI answer engines have different goals.
- **No blind scripts**: UI/UX Pro Max search.py, external setup/CLI, upstream hooks and dynamic instruction-fetch patterns were **not imported or executed**.
- **Context**: only installed profile descriptions are visible by default; SKILL.md has routing logic, references carry local procedures, and no external catalog is mounted.
- **Compliance**: all local skill text is independently authored synthesis, with pinned URLs for methodological inspiration; no vendor graphics/font assets are redistributed.
- **Limitations**: repository-level license status does not establish permissions on every upstream dataset; a later import must verify exact license texts/NOTICE and scripts per file. Static CI does not prove aesthetic quality, live accessibility, search indexing or AI answer inclusion.

## How to update responsibly

Before adopting a newer upstream commit: diff the old and new pinned files; identify factual/methodological benefit; audit changed scripts/dependencies/license terms; write a targeted local reference update; test positive and negative triggers; avoid increasing default profile metadata unnecessarily. No silent updates.

See [progressive expertise contract](progressive-expertise.md), [expertise backlog](expertise-audit.md), and the repository's governance charter (managed externally, not silently inserted in the repository).
