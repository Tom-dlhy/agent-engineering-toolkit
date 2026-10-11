---
name: data-visualization-design
domain: design
version: "1.0.0"
description: >-
  Use when designing or reviewing the meaning, chart choice, comparability, uncertainty and accessible presentation of dashboards, KPIs or data visualizations. Do not use to install chart libraries, invent metrics, implement vendor-specific chart APIs or replace existing shadcn/MUI/provider templates.
---

# Data visualization design — choose meaning, reuse rendering

## Mandate and preflight
1. Determine the **user decision** supported by the visualization: comparison, trend, distribution, relationship, composition or status. If an existing table communicates it better, prefer the table.
2. Identify the data owner, aggregation grain, unit, denominator, time window, sample size, missing values, freshness and source. Ask `data/analytics-modeling` for metric/grain semantics rather than redefining SQL, ETL or KPI formulas here.
3. Inspect project manifest, lockfile, existing chart/metric components, design tokens, installed provider and licensed capabilities **before drawing or adding code**. Reuse existing primitives/templates first; do not introduce a second charting engine for a design preference.
4. Specify a **visualization contract**: question, data fields/types, supported chart family, axis/scale/baseline, grouping, formatting, contrast, accessible alternative, interactions and empty/error/loading states.
5. Choose an appropriate chart and visual encoding with explicit failure modes; avoid truncated bar baselines, unsupported dual axes, 3D decoration, inconsistent denominators and undisclosed filtering.
6. Hand off renderer-specific implementation to the **already installed** `skills/ui/<provider>` (or the selected chart package's verified official docs). Follow real package versions and component APIs; never fabricate `Base UI Chart` APIs.
7. Validate interpretation with realistic fixtures and edge cases: zeros/negative values, missing observations, outliers, changing filters, small screens, reduced motion, keyboard and non-color alternatives. Measure understanding if actual user evaluation is possible.

## Ownership: avoid duplicate libraries
- `data/analytics-modeling`: defines trustworthy metrics and aggregations; this skill never computes business truth on its behalf.
- `ui/shadcn-ui`: source-owned chart wrappers and installed Recharts, including shadcn Chart where available. Use its component contract; this skill does **not** implement Recharts.
- `ui/mui` and other chosen providers: their documented charts/visualizations and licensing. Never translate one provider's props to another by guesswork.
- `ui/base-ui`: headless interaction/form primitives, **not** an assumed standalone chart engine. A project may use Base UI primitives *inside* shadcn components; inspect actual `components.json`.
- `ui/ui-component-research`: component/API/interaction implementation only when specialized help is needed.
- `stacks/ui-library-selection`: evaluate a provider only if no suitable installed one exists and the requirement cannot reasonably be met.
- `design-system` owns brand/semantic tokens; `accessibility-wcag` owns formal conformance; `responsive-visual-qa` owns screenshots.

## Read only the relevant branch
- [Chart choice and encoding decisions](references/chart-selection-and-encoding.md) — **read when** choosing visual form, axes, aggregation or relative/absolute comparisons.
- [Metric integrity, uncertainty and truthful scales](references/truthful-metrics-and-uncertainty.md) — **read when** reviewing KPI denominators, scale distortion, uncertainty, missing data and filters.
- [Provider reuse, accessibility and release evidence](references/provider-reuse-and-accessibility.md) — **read when** handing off to shadcn/MUI/another installed provider, reviewing alternatives or chart interactions.

## Done
A visual specification tied to verified data, **existing provider components**, explicit tradeoffs, accessibility and validation. No automatic npm installation, chart reimplementation, provider switching, invented data or unmeasured "dashboard usability improved" claims.
