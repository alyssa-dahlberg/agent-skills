# Relevance rework — in progress

Status: steps 1–4 done and deployed, step 5 not started.

## Why

`ts_rank_cd` alone ranks short documents too highly, because normalisation divides by document
length and our titles are short. A three-word title matching two terms outranks a long, genuinely
relevant body. We saw this on the "invoice template" query, where a tag page beat the actual guide.

The fix is to normalise by field rather than by whole document, and to floor the title contribution
so a title match can't dominate on its own.

## Steps

1. ~~Add `SearchOptions.FieldWeights`~~ done
2. ~~Backfill the `documents_fts` column~~ done
3. ~~Switch ranking to per-field normalisation with a title floor~~ done, deployed 4 March
4. ~~Drop the old `rank_legacy` column~~ done
5. Tune the floor against the query log — not started

Ranking is per-field normalised with a title floor of 0.3. Weights are title 0.6, body 0.4. This is
live in production as of 4 March.

## Notes

The backfill has to run after the GIN index exists or it table-scans — see the index creation in
`src/SearchIndex.cs`. Took 40 minutes on prod.

Relevance is being reworked, the new scoring model normalises per field. Ranking weights are title
0.6, body 0.4. The title floor is 0.3.

Open question: should the floor be configurable per tenant? Parking this until step 5.
