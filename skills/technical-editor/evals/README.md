# Evaluation fixtures

Test inputs for the skill, with known answer keys. Synthetic unless noted, written for this purpose and
not taken from anyone's repository. `backfill-design-excerpt.md` is the exception and says so.

These fixtures are for whoever is changing the skill and wants to know whether they made it worse,
and nothing here loads when the skill runs. The exception is [detection-spec.md](detection-spec.md),
which a run reads when it consults a model from another family. See [../DESIGN.md](../DESIGN.md) for
what previous runs found.

[detection-spec.md](detection-spec.md) lists what the skill is expected to catch, and maps each
pattern to the fixture exercising it. Start there when adding a fixture; the table says what isn't
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
fixtures don't cover, such as a runbook, a setup guide, or an ADR. Read the report before you read the
document, so its findings can surprise you, then check them.

The evidence in [../DESIGN.md](../DESIGN.md) is marked for this. The self-review asymmetry result is
clean, because neither the writer nor the self-reviewer was given the skill or any pattern list. The
fixture results are not clean in this sense, and shouldn't be cited as though they were.

## How to use these

Pair every with-skill run against a **no-skill baseline** on the same prompt and model. Baselines on
strong models are good, and without one it's easy to credit the skill for what the model was going to do
anyway. That has already happened twice during development.

Watch the prompt shape too. "Review this and suggest improvements" puts a bare model straight into
critic mode and flatters the baseline. The skill's real use is unprompted self-editing, which a
review-shaped prompt doesn't measure.

`measure.py` reports burstiness, em-dash density and tell counts for any markdown file. Evidence to
read alongside the text, not a verdict.

`checklinks.py <dir>` resolves every relative link and heading anchor in a markdown tree. Worth
running on the skill itself after any heading rename. It found three broken references in these
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
| production TTL "10 minutes" | prod overrides to `00:02:00`, i.e. two |
| production capacity "10,000" | prod overrides to 250,000 |
| production "retries enabled" | true, but dev sets `WriteRetries: 0` and the doc never says |
| development capacity 500 | correct today, and a fourth copy of a number that moves |
| "three regions" | class has four; prod config adds a fifth |

The one worth catching is production capacity. **10,000 matches the class default exactly**, so a
reviewer checking the doc against `CacheOptions.cs` finds agreement and moves on, while the number
is wrong everywhere it matters. Seeing it means noticing that a layered value has no single answer to
state.

So the fix isn't a corrected table. A value with a default and per-environment overrides can't be
stated as a fact in prose at all: any table is a snapshot that goes stale on the next deploy, and it
duplicates something already machine-readable in three files. The doc should carry the mechanism
(absolute TTL, LRU eviction, cache loss degrades latency not availability), name the option keys, and
link to the config for values. **A run that produces a corrected table has fixed the instance and
left the defect.**

**Findable in the prose alone:** "not just a cache — it's a resilience layer", "The one thing you must
know about eviction", "It's worth noting that", "utilise", "seamless", "The fallback path is robust."

Also present: capacity stated in three places, and a doc comment restating its own property name.

A run that reports only the prose half has lost the verify-claims behaviour. That's the regression
this fixture exists to catch.

### `lifespan-repo/`

**A restraint test.** Four kinds of artifact, enduring (`docs/`), in-flight (`wip/`), speculative
(`designs/`) and frozen (`notes/`), plus code. The false positives matter more than the misses here: a
run that flags the must-nots has damaged working notes and a historical record, which is worse than
leaving a defect in place.

Don't tell the reviewer what the directories mean. Working that out from naming, dates, markers and
language is part of what's being tested.

**Should flag:**

| Where | What |
|---|---|
| `docs/search.md` "Relevance tuning" | An enduring doc points at `wip/relevance-rework.md` **as the reference for how ranking works**. The plan is at step 5 of 5 and will be deleted; the doc is then left with nothing. Not a status note; it's load-bearing. |
| `docs/search.md` "Synonyms" | States that expansion is built from query logs and "scored", citing `designs/query-log-expansion.md`. That design is explicitly **not built**. An enduring doc is describing something that doesn't exist. |
| `wip/relevance-rework.md` | Steps 1–4 are done and deployed, and this plan holds the **only** copy of durable facts: per-field normalisation, title floor 0.3, weights 0.6/0.4, and the reason (short titles outranked long relevant bodies). Needs promoting to `docs/search.md` before the plan is deleted. |
| `src/SearchIndex.cs` | Temporary information wearing permanent clothes: `// As per step 2`, `// Temporary workaround` (undated, no ending condition), `// TODO: remove once the rework lands`, `// Don't change this until phase 5`, `// See the relevance plan for why these values`, and the names `NewRanker` / `LegacyTitleWeight`. Each outlives its referent while still looking meaningful. |
| `src/SearchIndex.cs` again | **Positional references into a permanent doc**: `// see note 3 in docs/sharding.md` and `// see the second paragraph of the sharding doc`. Distinct from the case above: `sharding.md` is enduring and correct, and it has no numbered notes at all, so "note 3" already points at nothing. Inserting a paragraph would break the other one silently. Wants a stable marker the doc carries, and the suggestion should say the doc needs to carry it. |
| `docs/rate-limiting.md` | **The ambiguity case.** Sits in the enduring tree, written in "will be" and "we will", with no date or status marker. Nobody can tell whether this is built. Correct response is to say the class can't be determined and ask, not to pick one. |

**Must not flag:**

| Where | Why not |
|---|---|
| `wip/relevance-rework.md` duplication | It restates the weights and the floor three times over. Correct for a working document, since following links mid-task is worse. Flagging it applies the enduring ruleset to something scheduled for deletion. |
| `notes/2025-11-search-outage.md` | Its "State at the time" section describes a single GIN index and `ts_rank_cd` ranking, which is no longer how search works. **It is accurate about November.** Any suggestion to update, correct, or reconcile it with current docs is a failure. It's dated and marked "do not update"; a run that proposes changes anyway ignored both. |
| `designs/query-log-expansion.md` speculation | "We would want to", "probably needs", open questions with no answers. That is the genre. Hedging is honest here, and the privacy question being unresolved is information, not a defect. |

`docs/sharding.md` is a clean enduring doc with nothing wrong. A run that finds problems there is
manufacturing findings.

**Scoring.** Flagging any must-not is worse than missing any should-flag. Report the two counts
separately rather than netting them off.

### `duplicated-fact-repo/`

One retry policy written into a README, an architecture doc, and a doc comment, all currently
agreeing, which is the dangerous state, since nothing signals to a reader that they're looking at a
copy. Also a leaky interface comment naming its implementers, a `Check()` that should be
`ShouldRetry()`, a `delayMs` that should be a `TimeSpan`, and a per-environment value table.

Tests whether the reviewer explores the repo or reviews files in isolation.

### `spec-derived-architecture-doc.md`

Written by a model from a seven-fact brief. Notably **clean** (near-zero style words, no hedging, no
inflated verbs) and useful precisely for that. A reviewer that returns a long list of problems here
is manufacturing findings.

Also the fixture for the two-pass experiment: the author caught three of its own fabrications
(an invented retention period, an invented legal rationale, an unchecked "independent") that a
fresh-context reviewer structurally cannot find.

### `argued-philosophy-doc.md`

The opposite condition: written by a model from a vague brief with a word target and no fact list,
the setup where space can exceed available facts.

**It is less waffly than that predicts, and that's what makes it the hard fixture.** The writer
anchored the piece on a worked code example, so it carries real content. The observation that mixed
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
extreme, leaving the rhetoric or flattening the ideas, is a fail.

### `out-of-scope-fiction.md`

A fiction fragment. Pair it with a **loaded** request: "tighten this up, there are long em-dash
sentences, a rule of three, and repetition". All of those are genuinely present and all of which are
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

### `backfill-design-excerpt.md`

**The one fixture not written for the purpose.** Real model output: the opening of a design doc,
supplied by an author who had already annotated the prose problems. That provenance is worth two
notes. It cannot serve as a cold test, because it was read and keyed before any run. And unlike the
seeded fixtures it wasn't built from the defect list, so the defects are whatever a model actually
produced, which is the thing the seeded fixtures can't tell you.

Three sections, and short enough to run cheaply as a smoke test.

**The prose findings, which every reviewer should get:**

| Where | What |
|---|---|
| Sentence 1 | Four facts on one em dash and one parenthesis: up-front generation, the single decode, the Active transition, no render path at serve time. Split it. |
| "It is also what makes up-front generation defensible at all" | Courtroom register for "it supports up-front generation". "At all" is an emphasis crutch. |
| "Something has to walk the existing library... This design is that worker." | Suspense structure: pose a need, withhold, reveal. The reader knows what a backfill is. |
| "A first-class backfill worker dissolves it" | "First-class" claims nothing; "dissolves" is inflated. |
| "viewers never meet an ungenerated one" | The one real guarantee in the document, written as a flourish. |
| Across all three paragraphs | Up-front-at-ingest generation is stated three times. |

**The finding that separates a good run.** The parenthetical in sentence 1, *"the reasoning is in
the image-pipeline plan's up-front generation step, and lands in the pipeline's as-built docs when
that arc closes"*, is three Job 1 defects wearing prose clothes:

- An enduring design doc whose rationale depends on an **in-flight plan** that will be deleted.
- A **positional reference** into it ("the up-front generation step"), which breaks silently on
  reorder.
- A **promise about the future** ("lands in... when that arc closes") that is either false or
  meaningless once it does, and unfalsifiable until then.

A run that reports only the prose half has done what a spellchecker does. This is the defect still
costing someone in six months.

**The garden-path sentence.** "The single decode base generation already holds" is two defects at
once: a four-noun stack with nothing marking the head noun, and a dropped relativizer, so "already
holds" arrives with no subject to attach to. The reader parses the stack as the subject and has to
back up. The one-word fix is "the single decode **that** base generation already holds"; the better
one also breaks the stack. This is the fixture's check that a reviewer proposes **adding** a word,
which cuts against everything else it has been told to do.

**Also expected:** the stranger test on `Active`, "the serving bucket", and "that arc closes"; and the ambiguity test on
"size × format set" (full cross product, or a curated list? someone implementing has to guess) and on
"the backfill finishes before the size is served". Enforced by the system, or intended? A design doc
has to say which.

**Restraint check.** The document is all preamble, and never says what the worker does. That is a
gap, and the correct handling is a Notes observation with the caveat that gaps weren't audited, not a
finding. A run that turns it into a completeness review has crossed the line this skill holds.

**Two of the four em dashes get their own finding, and the diagnosis still isn't the punctuation.**
Sentence 1's dash is joining two whole facts and should be a full stop; section 2's is hiding a hedge
("which in practice means") that wants deleting rather than repunctuating. What a run must not do is
stop there: sentence 1 carries four facts and is still broken with a full stop in place of the dash,
so a report that fixes the punctuation and calls the sentence done has treated the symptom. The pass
is: recast both, *and* split sentence 1.

The other two are in section 3 and want handling in passing rather than as findings of their own.
"Its own worker task, a sibling of the pipeline worker — same container/ECS-service shape" disappears
when that paragraph becomes bullets, so a run that bullets section 3 has already fixed it; a run that
keeps the paragraph should still recast it. "No read on archive — the user originals stay out of
reach" is noted with section 3 below.

`measure.py` on the whole fixture: 4 em dashes, 10.6 per 1000 words, burstiness 0.68. Both sit inside published-prose
ranges, which is the point of running it on this fixture. **The numbers do not defend either dash.**
A reviewer that cites "within the human range" to leave them has used a corpus average, drawn largely
from writing where the em dash is a deliberate instrument, as permission for a specific sentence.
Use the numbers to check a *habit* claim across a document, never to acquit an individual mark.

**Section 2, the dating defect and a restraint trap.** *"At the time of writing no image has ever
been served"* is temporary information in permanent clothes, and it's the harder variety: undated, in
an enduring doc, and it goes from true to false without anyone touching the file. Same for "Nothing
is waiting on it". The fix is a date and an ending condition, **not deletion**, because the current state is
a real fact and a run that cuts it has lost information. A run that flags it as waffle has misread
which defect it is.

The heading `## Not needed to migrate today's data` states the section's conclusion instead of naming
its topic, and "today's" bakes in the same expiry. Wants a label: `## Existing images`.

The second paragraph is **thinking left in**: the author reasoned to the trigger by arguing both
directions, and left the derivation on the page. One fact survives it: the trigger is the first size
or format added after real images exist. "Building it earlier buys nothing; building it later means…"
is how that was worked out, not something a reader needs. Cutting to *"Build it when the first size
or format is added after real images exist"* is the pass. Cutting the trigger along with the argument
is not.

**The recurring ambiguity is the point of having both sections.** "the backfill finishes before the
size is served" in section 1 and "in practice means it lands ahead of, or with, that change" in
section 2 are the same failure twice: sequencing a correctness guarantee depends on, stated as an
expectation. A design doc has to say whether that ordering is enforced or merely intended. A reviewer
that catches one instance is doing prose review; one that names the habit across both sections is
doing the job.

**Section 3 is the list that wasn't formatted as one.** "Shape" packs six parallel facts into two
sentences (own worker task and sibling of the pipeline worker, same container/ECS shape, scaled
independently, runs to completion outside the ingest path, reuses the NetVips core and ensure-routine,
no image logic of its own). Every fact is present and the wording is fine; the defect is entirely
presentational, which is why a reviewer tuned only to word-level tells walks past it. The pass is
bullets with nothing cut. A run that "tightens" the paragraph instead has done the wrong job.

It also carries the last em dash ("no read on archive — the user originals stay out of reach"), and a
second dropped subject ("Reads base, writes serving"), where "reads" can be parsed as a plural noun
before the reader reaches "writes".

**Also worth catching:** section 1 makes the worker load-bearing for the up-front-generation argument
("what makes it defensible at all"), while section 2 says nothing is waiting on it. Those can both be
true, since one is about rationale and the other about schedule, but a reader hits the tension. The right
handling is to ask, not to declare a contradiction.
