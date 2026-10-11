# RAG ingestion, structural chunks and provenance

**Read when:** extracting PDFs, HTML, tickets or internal
documents into chunks and vector/lexical indexes.

## Corpus input contract
Identify lawful owner/source, tenant and ACL metadata,
version and content hash, extraction timestamps, retention,
deletion obligations and update cadence. Preserve tables,
headers, captions, page numbers and structure; lossy OCR can
make a confident but wrong answer. Never store raw sensitive
documents in diagnostic logs.

## Chunking
Prefer semantic/structural boundaries (paragraph, heading,
table, section) before arbitrary fixed token windows.
Benchmark size/overlap for real question distributions and
model tokenizer. No universal chunk size. Keep stable
source ID, doc revision and offsets in chunk key for citations.
Overlap may improve recall but inflate context, index
storage and near-duplicate rankings.

## Embedding versions
Record model ID, dimensions, normalization, distance metric
and language coverage. Mixing unversioned embeddings from
different models can invalidate nearest-neighbor distances.
Embeddings derived from PII may themselves be sensitive data.

## Recovery
Stage new index revision before publication; reindex source
changes idempotently, tombstone deletes, invalidate caches and
test source-version alignment. An embedding call success
does not mean every replica has published the document.

Sources: https://docs.llamaindex.ai/en/stable/module_guides/loading/ ,
https://docs.langchain.com/oss/python/integrations/text_splitters/ .
