# Plain language

How to weigh what you find, and what not to cut.

This is deliberately not a list of patterns to scan for. Current models recognise the usual tells
without being shown a catalogue, and arriving with one turns a reading into a search — you find what
is listed and walk past what isn't. What's hard is judging what a pattern costs *this* reader in
*this* sentence, which is what this file is about.

## How to weigh what you find

**This is a list of things worth looking at, not a list of things to remove.** Read it the way you'd
read a style guide you respect and still argue with: it names the patterns that usually indicate the
writer stopped short of a fact, and it's wrong in specific cases often enough that applying it
without thinking makes writing worse. Every entry below is the right choice somewhere. Deciding
which case you're in is the actual work, and it's why this runs on a model with judgement rather than
a regex.

**Density is the signal.** Every pattern below appears in good human writing occasionally. Em dashes
are normal punctuation. "Robust" is sometimes exactly right. What makes prose tiring is these
patterns stacking: three in a paragraph, the same sentence shape four times running, every heading
doing a little bit of selling.

So don't sweep for banned words. Flag a pattern when you can say what it costs this reader in this
sentence. A suggestion that only cites a rule will get ignored, and deservedly.

**Count it when you claim density.** If a pattern is a habit rather than an instance, say how often —
"95 em dashes across 185 lines", "the *not X, but Y* frame five times in one document", "eleven of
the fourteen entries end with the same sentence". Grep or count for real; don't estimate. A number
turns a matter of taste into an observation the author can check, and it's the difference between
"this feels em-dashy" (arguable, ignorable) and evidence. It also protects you from the opposite
error: count first, and you'll sometimes find the habit you were about to flag occurs twice.

**Rhythm gives writing away more reliably than vocabulary.** Word lists are easy to check and easy to
evade, and they date fast. Sentence *shapes* are what a reader actually notices, and models produce
them regardless of which words are in play. Weight a rhythm you can point to above a word on a list.

**The underlying diagnosis is almost always the same:** the sentence isn't committing to a fact. The
flourishes fill the space where the fact should be. So the fix is usually "say the concrete thing",
not "use a different word".

## Human first drafts

Most of this file catalogues machine writing, because that's what needs cataloguing — the patterns
are consistent and easy to miss. Human drafts fail differently, and just as often. Everything here
applies to them too.

**Nobody's first cut is finished.** People write to work out what they think, dictate notes between
meetings, and leave in the scaffolding they used to get to the point. That's how drafting works, and
it isn't a criticism of the writer. But it means a document that was never edited will have these
in it:

- **Rambling and digression.** A paragraph that starts on one topic, follows an association, and
  ends somewhere else. Split it, and move the digression to where it belongs or cut it.
- **Buried lede.** The actual point arriving in the last sentence, after the reasoning that produced
  it. Readers want the conclusion first, then the support. This one is worth checking on every
  section — it's the most common structural problem in human writing and the easiest to fix.
- **Restarted sentences.** "The thing is, when you're setting this up — well, what actually matters
  is the pool size." The writer changed direction mid-sentence and never went back. Keep the second
  half.
- **Repetition from forgetting.** The same point made twice at a distance, in different words,
  because the writer lost track. Different from machine repetition, which restates immediately and
  deliberately. Merge them, and keep the clearer wording.
- **Unclear referents.** "This", "that", "it" pointing at something three sentences back or at a
  whole preceding idea. Cheap to fix and disproportionately costly to read past.
- **Thinking left in.** "I guess", "not sure what to call this", "perhaps", "anyway", "does that make
  sense". Honest while drafting, noise once the thing is decided. If the uncertainty is real and
  matters, state it as a fact: "the retry count here is a guess; we haven't measured it."
- **Verbal tics from dictation.** Filler openers, false starts, "sort of", "basically", "kind of",
  and long sentences held together by "and" and "so" because speech doesn't have full stops. Text
  that was spoken needs the heaviest structural edit — the ideas are usually sound and the shape is
  usually wrong. Bullets often recover a dictated list better than sentences do.

**Handle these with the same directness and no more.** A messy draft usually means the writer was
thinking hard about the subject and left the packaging for later, which is the right order to do it
in. Your report doesn't need to soften findings, and it also doesn't need to note that the writing
was rough — say what to change and why. The one thing to be careful of: human drafts carry more real
knowledge per confusing sentence than machine drafts do. Where a rambling passage contains a fact you
can't place, ask about it rather than cutting it.

## Headings

Headings are navigation. A reader scans them to decide where to go, so a heading's only job is to
name what's underneath it accurately.

| Instead of | Write |
|---|---|
| The one reviewed exception: Cloudflare Turnstile | Exception: Cloudflare Turnstile |
| Why this matters for this project specifically | Why |
| No savings plan — everything on demand, deliberately | On-demand pricing |
| A deep dive into the caching layer | Caching |
| Getting started is easy | Getting started |

Signs a heading has the wrong job: it's a full sentence, it contains a dash carrying a second clause,
it tries to make the section sound interesting, or it argues a position. Headings that read like
listicle titles ("The one trick...") borrow their shape from writing that has to compete for a click,
which documentation doesn't.

### Headings are labels, not descriptions

A heading is an index entry. A reader scanning a contents list wants the *name of the category*, in
the form they'd search for it. These habits break that, both common in generated docs:

**Starting with "The".** The definite article names one specimen instead of the class. It also reads
as the opening of a sentence, so the eye keeps going instead of stopping to file it.

| Written | Should be |
|---|---|
| The fact written three times | Repeated facts |
| The comment that restates the code | Comments restating code |
| The interface comment that leaks | Leaky interface comments |
| The call chain written out longhand | Call chains as prose |

**Describing instead of naming.** A heading built as a relative clause ("...that leaks", "...which
should be a link") is a sentence fragment doing a noun's job. Compress it to the noun phrase. If that
loses something the reader needs, the something belongs in the first line of the section, where
there's room for it.

Keep the article when the heading names one specific thing the section goes on to define, rather than
a category of them. `## The change test` is a name; `## The comment that restates the code` is a
description wearing one.

The test: could this heading be an entry in an index, or a row in a summary table? If reading it
aloud makes you want to finish the sentence, it isn't a label yet.

This also applies to coined names for concepts. Naming a phenomenon is useful shorthand once a reader
knows it, and pure friction before that. If a heading names an idea the reader hasn't met, either use
a plain descriptive label or introduce the term in the first sentence beneath it.

## Rewrite moves

The recurring fixes, in rough order of how often they apply:

1. **Split an em-dash run-on** into separate sentences.
2. **Turn a clause pile into bullets.** Three parallel things in one sentence read better as three
   lines. Technical readers scan bullets; they don't scan compound sentences.
3. **Delete the sentence.** The most common correct fix.
4. **Replace the abstraction with the concrete fact.** "Improves reliability" → "retries failed
   writes three times".
5. **Give the number.** Any claim about size, speed, or frequency that doesn't have one is weaker
   than it looks.
6. **Rename the heading** to what's under it.
7. **Cut to the audience's level.** Delete the explanation of a concept the actual reader already
   has.
8. **Merge two sentences that say the same thing** in different words. Models often restate a point
   immediately after making it.

## What not to cut

Economy is a means, not the goal. Shortening a document by removing facts makes it worse.

- **Keep every fact**, including the awkward ones. If you can't fit a fact into the rewrite, say so
  rather than dropping it.
- **Keep the "why".** Reasoning behind a non-obvious decision is the least recoverable information in
  a codebase. It's terseness with the reasoning removed that produces documents nobody can act on.
- **Keep necessary qualifiers.** "Usually", "on Linux", "before v3" are facts, not hedging. The
  difference is whether removing the word would make the sentence false.
- **Keep domain terms.** Precision isn't jargon. Replacing a specific term with a general one to
  sound plainer loses information.
- **Don't flatten voice into a monotone.** The target is how a competent engineer writes when they're
  being clear, not a stripped register with no personality. Plain is about structure and word choice,
  not about draining the text.
- **Don't simplify the content.** Splitting a sentence is good; explaining a concept the audience
  already has is condescending and makes the document longer.
