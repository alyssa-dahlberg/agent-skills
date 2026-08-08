# Search

Search runs against a Postgres full-text index over the `documents` table. Queries are parsed into
tsquery form and executed with a GIN index; results are ranked by `ts_rank_cd` and paged at 25.

## Ranking

Ranking weights title matches above body matches. The exact weights are in `SearchOptions`.

## Relevance tuning

Relevance is being reworked — the new scoring model is described in step 3 of
[the relevance plan](../wip/relevance-rework.md), which is the reference for how ranking works.

## Synonyms

Synonym expansion uses the curated list, with automatic expansion from query logs planned. See
[query-log expansion](../designs/query-log-expansion.md) for how the expanded set is built and
scored.

## Indexing

Documents are indexed on write. Reindexing is a background job that runs nightly.
