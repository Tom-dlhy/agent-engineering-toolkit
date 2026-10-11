---
name: database-selection
domain: stacks
version: "0.1.0"
description: >-
  Use when choosing PostgreSQL, SQLite, MySQL, document storage, key-value stores, search engines or warehouses. Do not select a database on popularity alone.
---

# database-selection

## Workload
Characterize write contention, query shapes, relational consistency, search, geospatial, analytics, size, durability, team experience and hosting.
## Selection
Use PostgreSQL as a credible default for transactional relational requirements, SQLite for simple embedded/small workloads, caches for disposable derived data and warehouses for analytical workloads. Verify provider-specific limits, durability and concurrency.
## Portability
Separate domain interfaces from persistence concerns where switching would be valuable; recognize that SQL dialect, indexes, consistency guarantees and operational migration can still be expensive.
## Exit
Provide realistic schema examples, expected query patterns, backup/restore, migration and failure-testing strategy, plus reasons against alternatives.
