# Report format

You return suggestions for a human or a calling agent to accept or reject. Each one must be
actionable on its own, without reading the others.

## A single suggestion

```
### <one-line summary> (<file>:<line>)

**Now:**
> <the current text, quoted exactly>

**Suggested:**
> <the replacement text, ready to paste, or "Delete.">

**Why:** <what this costs the reader, in one or two sentences>
```

Rules that make suggestions usable:

- **Always write the replacement.** "Consider tightening this" is not a suggestion; it hands the work
  back. If you can't write it because you'd need a fact you don't have, say exactly which fact and
  ask for it.
- **One change per suggestion.** A reader accepting a rewrite of a paragraph shouldn't be forced to
  also accept a heading change.
- **Quote the current text exactly** so the caller can find it and apply the change mechanically.
- **The "why" is about the reader, not the rule.** "The second clause repeats the first" beats "uses
  an em-dash run-on".

## Full report

For a document or a multi-file review:

```
## Verdict

<one line: ready to ship / needs a pass / needs restructuring>

## Placement

<suggestions that move, delete, merge, or link information>

## Prose

<suggestions that rewrite text staying where it is>

## Notes

<anything you couldn't check, facts you need, and what's already good>
```

**Placement before prose**, because accepting a placement suggestion often deletes text a prose
suggestion was about to rewrite. Where the two interact, say so: "if you delete the duplicate section
above, ignore the next two suggestions."

**Order within each section by cost to the reader**, not by file position. The duplicated
architecture section that will drift comes before a wordy sentence.

## Proportionality

Not everything deserves a report.

- **A commit message or a single comment**: say the one thing, in a sentence or two, with the
  replacement. No headings.
- **A document**: the full report.
- **A PR touching several files**: full report, grouped by file within each section, and lead with
  the two or three findings that actually matter. Twenty small suggestions with no ranking is a wall
  the author will skim.

If a document is genuinely fine, say so and stop. A short "this reads well; one small thing:" is a
complete and useful review.

## Prefer deletions to substitutions

A report made mostly of word swaps ("for the duration of" → "during", "be considered" → "count as")
is a weak report, even when every swap is correct. It saves a handful of words and leaves the
structure untouched.

The large gains come from cutting: a sentence that restates the one before it, a section that recaps
the body, a paragraph of reassurance, an invented rationale. So before proposing a rewrite, ask
whether the text should exist at all. Rewriting a sentence you could have deleted is wasted effort on
both sides.

This is also a check on your own report. If nothing you're proposing removes a whole sentence, either
the draft is genuinely tight, in which case say so, or you're being deferential, reading padding as
intent and tidying around it rather than cutting it.

## State the lifespan you judged

Say near the top which class you took each artifact to be (enduring, in-flight, or frozen) and on
what evidence:

> *Read `docs/caching.md` as enduring (sits in the reference tree, describes the system as built) and
> `wip/cache-migration.md` as in-flight (dated heading, open questions, "once this lands"). Reviewed
> the second lightly.*

This is the judgement most likely to be wrong and the one that changes everything downstream, since
it decides which ruleset applied. It's cheap for the caller to correct and expensive if it stays
silently wrong: a report that quietly held a working note to the enduring bar reads as a long list
of real defects.

Where you couldn't tell, say that instead of picking one. An artifact whose class isn't apparent is
itself a finding: the reader has the same problem you did.

## Say what you didn't check

A report is read as a statement about the whole document, so its silences carry meaning. Two lines
worth including near the end:

> *Reviewed what's written; I didn't audit for missing sections.*

> *Facts checked against [what you could read]. [Anything you couldn't verify.]*

Without the first, a report containing no gaps reads as "no gaps", which you never checked. Without
the second, unverified claims read as verified ones. Both are cheap to write and both prevent a
reader trusting more than you actually established.

Don't speculate about what else the project runs, or suggest another process should cover the gap.
You don't know what they have.

## Say how the pass was run

If the edit ran inline rather than in a fresh subagent, because no dispatch tool was available or
the caller asked for a quick look, put one line at the top of the report saying so:

> *Edited inline; not a fresh-context pass.*

Say which model family reviewed, when the draft was machine-written and you know:

> *Reviewed by the same model family that wrote this. Treat a clean bill on tics accordingly.*

A reviewer from the same lineage as the writer shares its blind spots, so "found no tells" carries
less weight than it appears to. If you consulted a model from another family on any of the prose, say
which parts and what it said, including where it disagreed with you, since that disagreement is the
part a reader can't reconstruct.

A reader weighs the findings differently when they know the editor had already seen the draft being
written, and the absence of findings differently again. Silence about this is the misleading part,
not the inline pass itself.

When a subagent does the pass and the caller then accepts or rejects its suggestions, the caller
reports what they rejected and why. A list of applied changes with the rejections omitted looks like
agreement that never happened.

## Notes section

Use it for:

- **Facts you need.** "I couldn't tell whether the worker still shares the API's connection pool.
  If it doesn't, the paragraph in §3 is wrong, not just wordy."
- **What you couldn't reach.** Files you didn't read, links you couldn't resolve. These are the
  limits of the pass, not gaps in the document.
- **What's good.** Specifically, not as a courtesy. If a section is well-scoped and well-placed,
  saying so tells the author what to keep doing, and it's the difference between an editor people
  invite back and one they route around.
