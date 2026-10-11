# Hybrid retrieval, rerank and query-time access control

**Read when:** deciding vector vs lexical vs hybrid retrieval
and enforcing document permissions in query planning.

## Retrieval choices
Lexical/BM25 covers exact identifiers, rare names and terms;
dense vectors can match semantic paraphrases. Hybrid
reciprocal-rank fusion may improve both; reranking with
cross-encoder/model can improve quality at added latency.
Choose on gold recall@k/citation correctness and cost,
not "vectors are state of the art" by assumption.

## Security
Bind authenticated principal to allowed tenant/doc ACL
at search/query layer. Do not retrieve cross-tenant chunks
into prompt and ask the model to filter them. Revocation
requires cache invalidation and live permission recheck
even when embeddings remain in an older index snapshot.
Restrict raw object stores and source document URLs too.

## Context selection
Dedupe near-identical chunks; rerank authorized candidates,
select enough distinct evidence under prompt token budget,
and preserve source IDs, spans, revision for citations.
A retrieval relevance score is not model-grounded answer
certainty. If no adequate authorized evidence, abstain.

## Test
Exact invoice key missed by vector, paraphrase missed by
lexical, long user query, multilingual question, stale ACL,
deleted doc in cache, redundant chunks crowding context,
no-hit denial and reranker latency under load.

Sources: https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html ,
https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/ .
