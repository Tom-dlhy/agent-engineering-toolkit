# RAG security, index drift and end-to-end regression

**Read when:** monitoring stale retrieval, document deletes,
multi-tenant search, poisoned knowledge base or model/index upgrades.

## ACL is retrieval correctness
Permissions can change after embedding. Index document/chunk
with durable ACL provenance, and enforce authorization at query
time rather than trusting old index snapshot or a prompt
asking model not to reveal secrets. Test revoked access, one
tenant retrieving another's vector neighbor and group changes.

## Drift types
Source content vs indexed snapshot lag; embedding model
upgrade without reembedding; tokenizer/preprocessor change;
ranking score distribution shifts; new language/domain terms;
document deletions remaining in cached context and citations.
Record source/content hash, embedding version, index revision
and expected fresh-by time.

## Threats
Poisoned document says "ignore instructions"; malicious URL
inside retrieved snippet; wrong tenant-specific index filter;
OCR/metadata chunk crossing document boundary; corrupted
search cache; downstream tool receiving source text as command.
The fix needs access control/sandbox and content trust
separation, not a stronger prompt alone.

## Release gate
Run frozen gold queries across before/after index; validate
ranking and grounded citation, empty/negative ACL set and
deleted document never returned. Measure p95 and index
cost under representative load. If a regression occurs,
roll back to last validated index/model revision if privacy
deletes can still be enforced correctly.

Sources: https://genai.owasp.org/llmrisk/llm012025-prompt-injection/ ,
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/ .
