# Auto Loader — checkpoint, schema evolution and file version guarantees

Read when: configuring cloudFiles ingestion, schemaLocation, checkpoint, rescued data or restart behavior on Lakeflow.

## Source and file-identity contract
Identify cloud object prefix and service principal permissions, notification/listing mode, immutable filenames/versioning, expected file count and schema contract. Auto Loader stores discovered file state in a checkpoint and can provide exactly-once file processing into Delta. This guarantee is **not** business-key idempotence when two distinct files carry the same order or a producer retransmits content under a different name.

Important nuance from official FAQ: default cloudFiles.allowOverwrites is false. When source files are overwritten, version selection can be ambiguous; if true, latest version is processed but intermediate revisions may be skipped and notification/listing interactions can cause duplicates. Require immutable object keys whenever possible.

## Versioned example — direct Structured Streaming, not Lakeflow-managed

~~~python
df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "dbfs:/demo-only/orders/_schemas")
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .load("s3://demo-only/orders/")
)
# This only defines a read stream, not a running, safe or authorized job.
# The writer must supply its OWN durable checkpoint and sink idempotency.
~~~
The path is **placeholder-only**, not a usable bucket. In Lakeflow managed pipelines, schema/checkpoint handling may be automated, so avoid copying standalone checkpoint settings blindly.

## Schema drift and recovery
- addNewColumns can evolve schema then terminate the stream with UnknownFieldException; schedule a controlled restart and investigate type changes.
- Rescue unexpected data only when owner agrees on quarantine/quality thresholds. A rescued record still needs review; silent rescue ≠ correctness.
- failOnNewColumns suits strict producer contracts. Type widening and schemaHints may need runtime support.
- Each independent ingestion stream requires appropriate separate state. Changing checkpoint location is effectively starting new ingestion from a new identity and may reprocess.
- Never delete checkpoint/state or set allowOverwrites as a quick fix on production; first decide replay/dedupe, billing and source retention.

## Negative test oracle
Same event twice; same order in two names; overwritten object; column add/type change; malformed payload; missing cloud notifications; checkpoint loss; future/backfill overlap. Reconcile **published business keys** and current source manifest, not only ingested file count.

Sources: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader and https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema and https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/faq
