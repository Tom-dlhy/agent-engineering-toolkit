# UI category audit — official source verified patterns and anti-template rules

Date: **2026-10-11**. Governance: user-provided Agent Engineering Toolkit
charter v2. Current main: 144 skills, 20 profiles, 12 domains.
Starting UI domain: 36 skills = 35 provider specialists + one
cross-vendor ui-component-research, each already has substantial
progressively read references (35×2 + 4 = 74 original UI leaves).

## Audit outcome — MODIFY, not inflate

No new provider skill. The repository already covers 35 installed
opt-in libraries for React, Vue, Angular, Svelte, Tailwind/HTML,
Web Components, React Native and Flutter, with specific APIs in
component-patterns and integration-and-verification. Adding another
"anti-slop" skill would duplicate **design/frontend-design**,
already present and routed by /anti-ai-slop. Similarly,
stacks/ui-library-selection already owns provider choice.

Changes:
- 35 provider SKILL.md entries enhanced with version-specific
  migration/composition/style distinctions and explicit design-skill
  hand-off; Base UI's obsolete package reference corrected.
- 8 high-risk vendor integration leaves updated (shadcn,
  Base, Chakra, HeroUI, MUI, PrimeVue, Skeleton, Bits).
- ui-component-research extended with one *compatibility/release*
  reference to own correct UI integration independently of art
  direction; its total is now **5**.
- design/frontend-design strengthened with a third *art direction and
  critique* reference (now 3) and honest two-pass brief→render review.
- No extra runtime profiles or catalogue entries, no maturity ranking.
**UI: 36 skills, 75 targeted leaves; Design frontend: 3 leaves.
Catalog: 144 skills, 20 profiles.**

## Checked upstream evidence (specific high-risk facts)

| Concern | Official provider/source | Decision |
|---|---|---|
| shadcn semantic token pairs | https://ui.shadcn.com/docs/theming | Token foreground/background pairs; never blindly overwrite local source components |
| shadcn Base/Radix | https://github.com/shadcn-ui/ui/blob/main/skills/shadcn/rules/base-vs-radix.md | Base render differs from Radix asChild; inspect components.json |
| Base UI composition | https://base-ui.com/react/handbook/composition | Official package @base-ui/react; render element forwards props/ref |
| Chakra v3 migration | https://chakra-ui.com/docs/get-started/migration | Flat v2 API/props replaced by compound parts/recipes/changed provider |
| HeroUI v3 | https://heroui.com/en/docs/react/getting-started/quick-start | Requires React 19+/Tailwind 4, different version contracts from v2 |
| HeroUI skill | https://heroui.com/en/docs/react/getting-started/agent-skills | Official skills exist, but no curl-pipe-shell/third-party installer executed |
| MUI X license | https://mui.com/x/introduction/licensing/ | MIT Community vs commercial Pro/Premium |
| PrimeVue v4 | https://v4.primevue.org/theming/styled/ | 3-tier tokens/presets and separate unstyled mode |
| Bits UI | https://bits-ui.com/docs/getting-started | Svelte 5 headless primitives, framework-specific state API |
| Skeleton | https://www.skeleton.dev/docs/svelte/get-started/installation | Tailwind v4 integration and explicit Flowbite/daisyUI conflict |
| APG Dialog | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ | Escape/focus containment/restore, proper accessible name |
| WCAG 2.2 AA 2.5.8 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum | At least 24×24 CSS pixels or documented exceptions |
| Native accessibility | https://docs.flutter.dev/ui/accessibility/accessibility-testing | Real mobile accessibility scanners and text scaling needed |

Other existing provider skills retain their respective official
documentation URLs; their descriptions clarify version and
platform decisions but **not every live combination or API in 35
vendor ecosystems was independently executed or reverified**.
A source link is a research lead, not proof of compatible behavior.

## Github skills research — use inspiration, avoid imports

- **Anthropic maintained Frontend Design**:
  https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md .
  A concise factual brief and explicit counterfactual design
  critique are useful; no blanket font/color ban. The method
  was rewritten into the already existing frontend-design skill.
- **Vercel Web Interface Guidelines**:
  https://github.com/vercel-labs/web-interface-guidelines .
  Emphasis on concrete feedback, labels, keyboard, forms,
  focus and responsive quality informs the release rubric.
- **Official shadcn UI agent skill/rules**:
  https://github.com/shadcn-ui/ui/tree/main/skills/shadcn .
  Source-owned UI, CLI diff and Base-vs-Radix rules enrich the
  existing shadcn-ui skill.
- **Official HeroUI skills**:
  https://heroui.com/en/docs/react/getting-started/agent-skills .
  The installer and any remote arbitrary commands are
  deliberately not executed; only document-backed distinctions
  are reused in original prose.

No remote SKILL.md, bundled executable or protected material
was copied. An actual external import needs source/license/
dependency and trust audit per governance.

## Operational definition of anti-AI-slop

Not a classifier and not a fixed prohibition on Inter/gradients/cards.
The objective is factual content, product-specific information
architecture and type/spacing/imagery system, functioning controls
and visually demonstrated craft. For a patch, don't rebrand. For a
new surface, use brief→one visual direction→counterfactual
critique→implementation→real browser critique. Never replace
established approved art direction for novelty.

## Validation and explicit unknowns

- Existing UI provider tests must remain green.
- New static contracts verify all 35 provider hand-offs, 75 UI
  references, Base package correction and verified source links.
- New qualitative evaluation briefs test that distinctly
  different products produce different art directions without
  inventing facts or hiding broken controls.
- No screenshots or rendered E2E for **all** vendors were run;
  these require actual app dependency versions and Playwright/
  device builds. Static Markdown QA cannot prove premium
  aesthetics, keyboard operability or production-safe native
  behavior. Post-PR follow-up should audit real product
  screenshots and component states against the rubric.

Draft PR only, no merge.

**SOTA means** version-accurate, source-grounded, scoped and actually
verified recommendations, never a generic visual score or a claim that
all 35 vendor integrations were executed in a real project.
