---
name: rag-engineering
domain: ai
version: "0.1.0"
description: >-
  Use when implementing RAG document ingestion, chunking, embeddings,
  hybrid search, ACL-aware indexing, reranking, source provenance,
  citation assembly and index lifecycle. Do not substitute for
  retrieval evaluation or generic SQL storage choices.
---

# RAG engineering — secure retrieval and document lifecycle

## Procedure
1. Establish corpus authority, ingestion rights, tenant/ACL model,
   source versions, deletion retention and real question patterns.
2. Extract/normalize documents with structure, page/section metadata
   and durable source IDs. Preserve original timestamps and provenance.
3. Choose segmentation/chunking from content boundaries and gold query
   experiments; do not impose a universal chunk size or overlap.
4. Select embeddings, sparse lexical retrieval and hybrid/rerank based
   on measured recall, query languages and cost; keep embedding model
   version, dimensions and distance metric consistent across index.
5. Enforce ACL and tenant filter **before results are returned to model**;
   inaccessible chunks cannot be allowed into prompt and then censored.
6. Build grounded context with source offsets, version and deterministic
   citations; treat retrieved text as untrusted instructions.
7. Design incremental reindex, deletes/tombstones, consistency lag,
   cache invalidation and controlled rollback of index/model versions.

## References
- [Ingestion, chunking and metadata lineage](references/ingestion-and-chunking.md)
  — **read when** building extraction, segmentation or indexing.
- [Hybrid retrieval, reranking and ACL](references/hybrid-search-and-access.md)
  — **read when** designing search plan, filters and context selection.
- [Index lifecycle, freshness and safe citations](references/index-lifecycle-and-grounding.md)
  — **read when** migrating embedding models, handling deletes or citing sources.

## Ownership
rag-evaluation tests recall/grounding; agent-tool-safety validates
tool/retrieved trust boundaries; data-pipeline-quality owns generic
batch lineage; llm-integration owns final provider generation contract.

## Done
Versioned index, source ACL propagation, query/rerank choices backed
by gold tests, delete/reindex strategy and grounded answer contract.
