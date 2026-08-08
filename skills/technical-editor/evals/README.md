# Evaluation fixtures

Test inputs for the skill, with known answer keys. All synthetic — written for this purpose, not
taken from anyone's repository.

Nothing here is loaded when the skill runs. It's for whoever is changing the skill and wants to know
whether they made it worse. See [../DESIGN.md](../DESIGN.md) for what previous runs found.

[detection-spec.md](detection-spec.md) lists what the skill is expected to catch, and maps each
pattern to the fixture exercising it. Start there when adding a fixture — the table says what isn't
covered.

## Run fixtures in isolation

**This file is an answer key sitting next to its own fixtures.** A reviewer following the skill
explores the neighbourhood of whatever it's pointed at, so aimed at a fixture in place it will read
this file and score well for the wrong reason. That has already happened; the run disclosed it, which
is luck rather than a safeguard.

So copy the fixture out before every run:

```bash
./isolate.sh doc-code-drift-repo      # prints a path under a fresh temp dir
```

Give both arms of a comparison the same treatment. An asymmetry here is worse than contamination in
both, because it looks like a result.

## What these fixtures cannot tell you

**They are regression tests, not evidence the skill works.** Every one was built by seeding defects
from a list the author had already written, so a run that finds them has found what was planted.
That is circular as proof of capability, and it is fine for the job fixtures actually do: telling you
whether a change made things worse.

The claim they cannot support is the one people will want them to: *"the skill is good at reviewing
documents."* For that you need documents nobody involved constructed or read first. Judging a report
against your own expectations, when those expectations produced the fixture, measures agreement with
yourself.

So keep at least one **cold test** in rotation: a real document from a real repo, ideally a kind the
fixtures don't cover — a runbook, a setup guide, an ADR. Read the report before you read the
document, so its findings can surprise you, then check them.

The evidence in [../DESIGN.md](../DESIGN.md) is marked for this. The self-review asymmetry result is
clean, because neither the writer nor the self-reviewer was given the skill or any pattern list. The
fixture results are not clean in this sense, and shouldn't be cited as though they were.

## How to use these

Pair every with-skill run against a **no-skill baseline** on the same prompt and model. Baselines on
strong models are good — without one it's easy to credit the skill for what the model was going to do
anyway. That has already happened twice during development.

Watch the prompt shape too. "Review this and suggest improvements" puts a bare model straight into
critic mode and flatters the baseline. The skill's real use is unprompted self-editing, which a
review-shaped prompt doesn't measure.

`measure.py` reports burstiness, em-dash density and tell counts for any markdown file. Evidence to
read alongside the text, not a verdict.

`checklinks.py <dir>` resolves every relative link and heading anchor in a markdown tree. Worth
running on the skill itself after any heading rename — it found three broken references in these
files, in a skill whose own advice is that a link which stops resolving is the visible signal that
keeps a document honest. A reviewer should still check links by hand where it matters, since this
catches dead targets but not references that now point at the *wrong* thing, which is the failure
mode [reference by identity](../reference/information-architecture.md#reference-by-identity-not-position)
is about.

## Fixtures

### `doc-code-drift-repo/`

The most useful regression test here, because the answer key is unambiguous. A caching doc that
disagrees with `CacheOptions.cs` in six ways, plus six catalogued prose tells.

**Requires reading the code:**

| Defect | Truth |
|---|---|
| "expire after 5 minutes" | `Ttl` default is 600s |
| "of inactivity" (sliding) | doc comment says absolute, reads don't extend |
| "three regions" | `Regions` has four |
| "retried a few times" | `WriteRetries` is 2 |
| link to `replication.md` | file doesn't exist |
| "the oldest entry is dropped" | policy is least-recently-used; different entry |

**Requires reading the config, which is where this gets interesting.** `CacheOptions` holds defaults,
`appsettings.json` sets a base, and `appsettings.Production.json` / `appsettings.Development.json`
override per environment. The doc's `## Environments` table restates all of it, and is wrong in ways
a doc-versus-class check cannot see:

| Doc says | Actually |
|---|---|
| production TTL "10 minutes" | prod overrides to `00:02:00` — two |
| production capacity "10,000" | prod overrides to 250,000 |
| production "retries enabled" | true, but dev sets `WriteRetries: 0` and the doc never says |
| development capacity 500 | correct today, and a fourth copy of a number that moves |
| "three regions" | class has four; prod config adds a fifth |

The one worth catching is production capacity. **10,000 matches the class default exactly**, so a
reviewer checking the doc against `CacheOptions.cs` finds agreement and moves on — while the number
is wrong everywhere it matters. Seeing it means noticing that a layered value has no single answer to
state.

So the fix isn't a corrected table. A value with a default and per-environment overrides can't be
stated as a fact in prose at all: any table is a snapshot that goes stale on the next deploy, and it
duplicates something already machine-readable in three files. The doc should carry the mechanism —
absolute TTL, LRU eviction, cache loss degrades latency not availability — name the option keys, and
link to the config for values. **A run that produces a corrected table has fixed the instance and
left the defect.**

**Findable in the prose alone:** "not just a cache — it's a resilience layer", "The one thing you must
know about eviction", "It's worth noting that", "utilise", "seamless", "The fallback path is robust."

Also present: capacity stated in three places, and a doc comment restating its own property name.

A run that reports only the prose half has lost the verify-claims behaviour. That's the regression
this fixture exists to catch.

### `lifespan-repo/`

**A restraint test.** Four kinds of artifact — enduring (`docs/`), in-flight (`wip/`), speculative
(`designs/`), frozen (`notes/`) — plus code. The false positives matter more than the misses here: a
run that flags the must-nots has damaged working notes and a historical record, which is worse than
leaving a defect in place.

Don't tell the reviewer what the directories mean. Working that out from naming, dates, markers and
language is part of what's being tested.

**Should flag:**

| Where | What |
|---|---|
| `docs/search.md` "Relevance tuning" | An enduring doc points at `wip/relevance-rework.md` **as the reference for how ranking works**. The plan is at step 5 of 5 and will be deleted; the doc is then left with nothing. Not a status note — it's load-bearing. |
| `docs/search.md` "Synonyms" | States that expansion is built from query logs and "scored", citing `designs/query-log-expansion.md`. That design is explicitly **not built**. An enduring doc is describing something that doesn't exist. |
| `wip/relevance-rework.md` | Steps 1–4 are done and deployed, and this plan holds the **only** copy of durable facts: per-field normalisation, title floor 0.3, weights 0.6/0.4, and the reason (short titles outranked long relevant bodies). Needs promoting to `docs/search.md` before the plan is deleted. |
| `src/SearchIndex.cs` | Temporary information wearing permanent clothes, five ways — `// As per step 2`, `// Temporary workaround` (undated, no ending condition), `// TODO: remove once the rework lands`, `// Don't change this until phase 5`, `// See the relevance plan for why these values`, and the names `NewRanker` / `LegacyTitleWeight`. Each outlives its referent while still looking meaningful. |
| `src/SearchIndex.cs` again | **Positional references into a permanent doc** — `// see note 3 in docs/sharding.md` and `// see the second paragraph of the sharding doc`. Distinct from the case above: `sharding.md` is enduring and correct, and it has no numbered notes at all, so "note 3" already points at nothing. Inserting a paragraph would break the other one silently. Wants a stable marker the doc carries, and the suggestion should say the doc needs to carry it. |
| `docs/rate-limiting.md` | **The ambiguity case.** Sits in the enduring tree, written in "will be" and "we will", with no date or status marker. Nobody can tell whether this is built. Correct response is to say the class can't be determined and ask — not to pick one. |

**Must not flag:**

| Where | Why not |
|---|---|
| `wip/relevance-rework.md` duplication | It restates the weights and the floor three times over. Correct for a working document — following links mid-task is worse. Flagging it applies the enduring ruleset to something scheduled for deletion. |
| `notes/2025-11-search-outage.md` | Its "State at the time" section describes a single GIN index and `ts_rank_cd` ranking, which is no longer how search works. **It is accurate about November.** Any suggestion to update, correct, or reconcile it with current docs is a failure. It's dated and marked "do not update"; a run that proposes changes anyway ignored both. |
| `designs/query-log-expansion.md` speculation | "We would want to", "probably needs", open questions with no answers. That is the genre. Hedging is honest here, and the privacy question being unresolved is information, not a defect. |

`docs/sharding.md` is a clean enduring doc with nothing wrong. A run that finds problems there is
manufacturing findings.

**Scoring.** Flagging any must-not is worse than missing any should-flag. Report the two counts
separately rather than netting them off.

### `duplicated-fact-repo/`

One retry policy written into a README, an architecture doc, and a doc comment — all currently
agreeing, which is the dangerous state, since nothing signals to a reader that they're looking at a
copy. Also a leaky interface comment naming its implementers, a `Check()` that should be
`ShouldRetry()`, a `delayMs` that should be a `TimeSpan`, and a per-environment value table.

Tests whether the reviewer explores the repo or reviews files in isolation.

### `spec-derived-architecture-doc.md`

Written by a model from a seven-fact brief. Notably **clean** — near-zero style words, no hedging, no
inflated verbs — and useful precisely for that. A reviewer that returns a long list of problems here
is manufacturing findings.

Also the fixture for the two-pass experiment: the author caught three of its own fabrications
(an invented retention period, an invented legal rationale, an unchecked "independent") that a
fresh-context reviewer structurally cannot find.

### `argued-philosophy-doc.md`

The opposite condition: written by a model from a vague brief with a word target and no fact list —
the setup where space can exceed available facts.

**It is less waffly than that predicts, and that's what makes it the hard fixture.** The writer
anchored the piece on a worked code example, so it carries real content — the observation that mixed
altitude costs *trust in the text* rather than just attention is a genuine idea, and the argument that
a lower-altitude detail implies significance it may not have is worth keeping. A reviewer that strips
this document to bullet points has destroyed it.

The padding is real but rhetorical rather than lexical: antithesis frames ("Neither position is
wrong. What is wrong is…", "doesn't only cost X; it costs Y"), a dramatic "This is the real damage.",
and a metaphor extended past its usefulness. `measure.py` against
`spec-derived-architecture-doc.md`: em dashes 11.8 vs 9.4 per 1000 words, emphasis crutches 3 vs 0,
inflated verbs 2 vs 0. Modest, and consistent with rhythm giving writing away more reliably than
vocabulary.

Use it to check that a reviewer can separate padding from argument. Cutting the flourishes while
keeping the code example, the trust point, and the implied-significance argument is the pass. Either
extreme — leaving the rhetoric or flattening the ideas — is a fail.

### `out-of-scope-fiction.md`

A fiction fragment. Pair it with a **loaded** request — "tighten this up, there are long em-dash
sentences, a rule of three, and repetition" — all of which are genuinely present and all of which are
load-bearing.

Correct behaviour: say the skill's rules don't apply, explain what each feature is doing, **and do the
edit anyway** with ordinary editorial judgement. A bare refusal is a failure; an earlier version
scored worse than the no-skill baseline here.

### `inflated-commit-message.txt`

Ten lines with "it's not just X", "fundamentally", a file-by-file inventory duplicating the diff, and
"chosen deliberately". Point it at `duplicated-fact-repo/`, which the message describes.

Tests proportionality. A structured multi-section report for ten lines is the failure, however
correct the findings. It should also notice that the backoff schedule already exists three times in
that repo and shouldn't be restated a fourth.
