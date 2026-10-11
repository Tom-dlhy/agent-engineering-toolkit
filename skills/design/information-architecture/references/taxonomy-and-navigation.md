# Taxonomy, product navigation and user vocabulary

Read when: designing a route hierarchy, menus, breadcrumbs, content taxonomy or findable destination labels.

## Inventory to tree
List actual content objects and user tasks before grouping. For each proposed node record ID, label, description, parent, synonyms, owner, permission, canonical destination and primary user question. Avoid designing IA purely from internal company departments.

```text
Account
  Profile
  Billing
  Security
Projects
  Active
  Archived
Support
  Help articles
  Contact
```
This is a hypothetical example. Do not invent these pages in a target project. Prefer stable routes with clear labels; breadcrumb follows logical location, not necessarily navigation history.

## Test information scent
Ask "where would a first-time user look for past invoices?" and see if labels and grouping lead to the known destination. Distinguish user-tested evidence from expert hypothesis. Consider cross-linked destinations when categories intersect, rather than duplicating content records. Search and navigation are complementary, not substitutes for clear labels.

## Engineering boundaries
Router controls path syntax, locale prefixes and actual page rendering; UI provider supplies Menu/Tabs/Breadcrumb components. This skill decides the conceptual location/label and migration acceptance, never rebuilds router or components.

Primary reference: https://design-system.service.gov.uk/patterns/navigate-a-service/
