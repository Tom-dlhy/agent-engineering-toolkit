---
name: information-architecture
domain: design
version: "1.0.0"
description: >-
  Use when designing or reorganizing a product's navigation, content taxonomy, search facets, labels, sitemap or findability across multiple destinations. Do not use for software module architecture, a one-off CSS grid, or editorial SEO calendars.
---

# Information architecture — findability before page layout

## Workflow
1. Inventory actual content, audience tasks, permissions, navigation/search analytics if authorized, and current routes/labels. Do not invent user research, taxonomy needs or pages.
2. Map top user questions to concrete destinations. Identify audience vocabulary and distinguish functional navigation from marketing copy.
3. Group material by user mental model and information relationships, not internal team structure; choose an explainable hierarchy, cross-links, facets and naming conventions.
4. Define a navigational contract: stable destination identity/URL, breadcrumb and current location, cross-level traversal, search/facet semantics, accessibility and permissions for hidden/restricted content.
5. Test ambiguous branches and "where would you look" questions via a representative tree-test protocol. If no participants are available, label the exercise as an internal heuristic walkthrough, not user research.
6. Reuse existing router/menus/search components. `frontend/<framework>` owns routing APIs, `ui/<provider>` owns menu/tab/combobox composition. Avoid rebuilding navigation primitives.
7. Document rollout and migration: redirects, deep links, bookmarks, route titles, analytics event continuity and navigation discoverability.

## Deep branches
- [Taxonomy, labels and navigation hierarchy](references/taxonomy-and-navigation.md) — **read when** reorganizing menus, navigation sections, page labels, breadcrumbs or route trees.
- [Search, filtering and facet design](references/search-and-facets.md) — **read when** choosing search fields, scopes, filters, empty results, ranking affordances or discoverability.
- [Tree-test planning and migration verification](references/tree-testing-and-migration.md) — **read when** validating findability or moving categories/routes in a live product.

## Ownership
`interaction-flow-design` owns the sequence **within** a task; this skill owns where tasks/content **live** and how users discover them. `growth/content-strategy` owns what editorial content to publish; `growth/technical-seo` owns crawler/sitemap mechanics. `architecture` owns source-code architecture.

## Result
A task-grounded map with label definitions, URL/permission considerations, tested or explicitly hypothetical findability claims and migration/verification plan.
