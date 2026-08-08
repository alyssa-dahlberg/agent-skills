# Query-log synonym expansion (design sketch)

Not built. Exploring whether we can mine synonyms from query logs instead of curating them by hand.

## Idea

Users who search for one term and then immediately search for another, then click a result, are
telling us the two terms are related. We could mine that co-occurrence and propose synonym pairs
above a confidence threshold.

## Open questions

- What confidence threshold? Probably needs to be tuned against a held-out set.
- Do we auto-apply above some threshold, or always review? Leaning toward always review — a bad
  synonym pair degrades every query containing the term.
- Privacy: query logs are user data. We would need to aggregate before anything is stored, and this
  probably needs a look from someone who knows the retention rules.

## Rough shape

A nightly job over the last 30 days of logs, producing candidate pairs into a review queue. Nothing
enters the live synonym list without a human accepting it.

We would want to measure this properly before and after — probably click-through on the affected
queries.
