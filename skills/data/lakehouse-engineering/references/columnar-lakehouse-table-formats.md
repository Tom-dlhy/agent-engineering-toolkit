# Parquet, Apache Iceberg and transaction-aware table format

**Read when:** choosing files, table metadata, snapshots,
schema/partition evolution or lakehouse compaction.

## Different layers, different guarantees
Parquet stores typed columnar data inside a file with row
groups and compression; a pile of Parquet files is not
automatically an ACID table. Iceberg is table metadata/
snapshot/manifest layer over data files, with atomic
table metadata commit where the catalog/engine supports it.
An analytic compute engine then executes queries against
files and metadata; specific features vary by engine.

## Iceberg evolution
Iceberg uses field IDs for safe schema changes and
supports partition spec evolution without immediately
rewriting old files. Old/new spec coexist, with planning
across specs. Changing partition spec does not guarantee
all historical files are laid out with new partitioning.
Check engine-specific supported Iceberg spec version,
catalog/REST credentials and schema evolution behavior.

## Physical layout
Choose file sizes and row group/compression by expected
scan and update workload, not a universal MB value.
Many small files increase planning/metadata IO; huge
files impede parallelism/rewrite. Compaction/rewrite
costs compute and storage; snapshots and orphan removal
must account for active readers and retention. Never
delete "old" object files just by listing timestamps
without table format snapshot reachability.

## Privacy and permissions
Object storage, catalog metadata and query engine access
are separate security layers. Policies/column masking
need to be enforced at actual reader interface;
presigned raw object access might bypass warehouse masking.
Test time travel/retention erasure and backup restore,
not assume expired snapshots disappear from all copies.

## Verification
Schema rename then old-file read, partition spec update
and old snapshot query, interrupted commit, concurrent
writer conflict, compaction during reader, lost credentials,
table metadata restore and unexpected high file count.

Sources: https://iceberg.apache.org/docs/nightly/evolution/ ,
https://iceberg.apache.org/spec/ ,
https://parquet.apache.org/docs/ .
