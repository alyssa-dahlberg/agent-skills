# Search outage, 12 November 2025

Written up the day after. Point-in-time record — do not update.

## What happened

Search returned 500s for 43 minutes starting 09:12 UTC. The nightly reindex job had been changed the
previous week to rebuild the GIN index concurrently, and the concurrent build failed partway,
leaving the index invalid. Postgres will happily plan against an invalid index and then error at
execution.

## State at the time

Search ran against the `documents` table with a single GIN index over a `tsvector` column, ranked by
`ts_rank_cd`, paged at 25. The reindex job ran at 02:00 daily. There was no check that the index was
valid before serving.

## What we did

Dropped and rebuilt the index non-concurrently, which took the search feature down for a further 8
minutes but restored service. Reverted the reindex change the same afternoon.

## What we changed afterwards

Added a validity check to the health endpoint. The reindex job now fails loudly rather than leaving
an invalid index in place.
