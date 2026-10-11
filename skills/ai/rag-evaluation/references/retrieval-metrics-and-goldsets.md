# RAG retrieval metrics, test questions and rankings

**Read when:** choosing retrieval@k metrics, evaluating
chunking/embedding/hybrid/rerank changes or constructing gold passages.

## Gold evidence
For each question record corpus snapshot, access tenant/scope,
answerable status, at least one accepted passage/span, semantic
equivalents, canonical source/version and annotation confidence.
Some questions require **multiple** distinct facts: define
whether full supporting-set recall or any passage counts as hit.

## Ranking metrics
Recall@k = number of relevant items retrieved divided by number
of relevant items; precision@k = relevant among top k divided by k,
under explicit treatment for short result lists. MRR measures
rank of first correct relevant result; nDCG captures graded ranking
where documents have varying relevance. Define unit (document,
chunk or passage) consistently or metric is misleading.

## Negative controls
No-authorized-answer questions should return **no unauthorized
chunks**, not artificially inflate recall with leaked passage.
Measure document ACL filter before similarity search/selection.
Cross-tenant and stale-index misses are correctness failures,
not only relevance errors.

## Experiments
Compare lexical BM25, vectors, hybrid fusion and reranker
using same frozen index/query set and query latency/cost.
Tune on development set; report results on held-out.
A model judge labeling synthetic generated questions can
bias evaluation toward its own phrasing; include real queries.

Sources: https://docs.llamaindex.ai/en/stable/module_guides/evaluating/ ,
https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html .
