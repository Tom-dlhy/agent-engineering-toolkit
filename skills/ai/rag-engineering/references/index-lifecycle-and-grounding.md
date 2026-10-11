# RAG index evolution, citations and safe rollback

**Read when:** moving to new embedding model, changing document
access, incrementally reindexing or emitting grounded citations.

## Deployment artifact
Version source snapshot, ACL revision, chunk algorithm,
embedding model/dimensions, index schema and query/rerank
settings. Build and test candidate index separately and
switch aliases only after recall/security tests. Rolling
back must not resurrect deleted/revoked content.

## Source deletion and freshness
Maintain source-to-index lag SLO, tombstones and event
revision monotonicity. Repeated or stale CDC events should
not make removed chunks live. Remove cached contexts and
source IDs when access is revoked; snapshot retention
can conflict with privacy policy and needs explicit review.

## Provenance and citations
Return document ID/version/page/section/source span. Model
text alone is not citation authority: resolve generated
citations against actual authorized source and check support
for each meaningful claim. When evidence is missing,
decline or state uncertainty. Avoid exposing source paths
that reveal private tenant structure.

## Negative regressions
Concurrent reindex/query, stale content with newer ACL,
deleted source appears after rollback, embedding schema
mismatch, missing passage offset, invalid cited ID,
long table split, index publication failure and
missing source owner.

Sources: https://platform.openai.com/docs/guides/retrieval ,
https://docs.llamaindex.ai/en/stable/module_guides/loading/ ,
https://genai.owasp.org/llm-top-10/ .
