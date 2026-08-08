# Plain language

How to weigh what you find, and what not to cut.

This is deliberately not a list of patterns to scan for. Current models recognise the usual tells
without being shown a catalogue, and arriving with one turns a reading into a search: you find what
is listed and walk past what isn't. What's hard is judging what a pattern costs *this* reader in
*this* sentence, which is what this file is about.

## How to weigh what you find

**This is a list of things worth looking at, not a list of things to remove.** Read it the way you'd
read a style guide you respect and still argue with: it names the patterns that usually indicate the
writer stopped short of a fact, and it's wrong in specific cases often enough that applying it
without thinking makes writing worse. Every entry below is the right choice somewhere. Deciding
which case you're in is the actual work, and it's why this runs on a model with judgement rather than
a regex.

**Density is the signal.** Every pattern below appears in good human writing occasionally. "Robust"
is sometimes exactly right. What makes prose tiring is these patterns stacking: three in a paragraph,
the same sentence shape four times running, every heading doing a little bit of selling.

**The em dash is the exception. Treat each one as a finding.** It has become the single most
overrepresented mark in machine prose, and the ordinary density rule under-reacts to it for two
reasons. It's contagious: writers who read a lot of model output start producing it, so a rising rate
in a repo is a habit being absorbed rather than a style being chosen. And it's usually a decision
that didn't get made. The dash joins two clauses without saying how they relate, which is exactly
the move a writer makes when they haven't worked out whether the second clause is a cause, a
consequence, an aside, or a separate fact. See [em dashes](#em-dashes) for what to do with one.

So don't sweep for banned words. Flag a pattern when you can say what it costs this reader in this
sentence. A suggestion that only cites a rule will get ignored, and deservedly.

**Count it when you claim density.** If a pattern is a habit rather than an instance, say how often:
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

Most of this file catalogues machine writing, because that's what needs cataloguing: the patterns
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
  section. It's the most common structural problem in human writing and the easiest to fix.
- **Restarted sentences.** "The thing is, when you're setting this up, well, what actually matters
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
  that was spoken needs the heaviest structural edit: the ideas are usually sound and the shape is
  usually wrong. Bullets often recover a dictated list better than sentences do.

**Handle these with the same directness and no more.** A messy draft usually means the writer was
thinking hard about the subject and left the packaging for later, which is the right order to do it
in. Your report doesn't need to soften findings, and it also doesn't need to note that the writing
was rough. Say what to change and why. The one thing to be careful of: human drafts carry more real
knowledge per confusing sentence than machine drafts do. Where a rambling passage contains a fact you
can't place, ask about it rather than cutting it.

## Em dashes

**Default to recasting every one.** Not a ban. The question to ask is what the dash is doing, and in
technical prose the answer is usually "standing in for a decision the writer didn't make". Work out
the relation between the two halves and use the punctuation that says it:

| The dash was hiding | Use |
|---|---|
| Two separate facts | A full stop |
| A cause or consequence | A full stop and *so*, *because*, *which means* |
| An aside the sentence can survive without | Brackets, or delete it |
| A definition or expansion of what precedes | A colon |
| A list of three parallel things | Bullets |
| Nothing, the clause is filler | Delete the clause |

**Recasting is not substitution.** Swapping the dash for a comma or a semicolon leaves the sentence
exactly as overloaded and only hides the evidence. If the fix doesn't change how the sentence is
built, it isn't a fix.

**Where one earns its place:** a genuine interruption that breaks the sentence's own grammar, or
setting off a phrase that already contains commas, where brackets would be too heavy. Both are rare
in documentation. A technical document with none reads perfectly well, which is not true of the
comma.

**Don't argue this from a corpus average.** Published-prose baselines include writing where the em
dash is a deliberate instrument, so "within the normal range" defends nothing about a specific
sentence. If you want a comparison, use the repo's own rate. A document well above its neighbours is
someone's habit arriving, and that's worth saying with a count.

**Report them as one finding, not twenty.** Where they're a habit, give the count, fix the two or
three worst sentences in full, and say the same move applies to the rest. Twenty separate entries for
the same punctuation mark buries everything else in the report.

**Say what it costs, not who wrote it.** "This sentence carries three facts joined by a dash; split
it" is a finding the author can act on. "This reads as AI-written" is an accusation, and it invites
an argument about provenance instead of a fix. The overload is the defect whoever typed it.

## Sentences that mislead on first read

A sentence can be perfectly grammatical and still send the reader down the wrong path, so they reach
the end, realise the structure wasn't what they assumed, and have to go back and re-parse. Linguists
call the extreme version a **garden-path sentence**; Joseph Williams calls the everyday version a
**miscue**. Either way the cost is the same, and it's a cost this skill cares about a lot: the reader
spends attention on decoding the sentence instead of on the fact inside it, and often can't say why
the document felt hard.

**This is the failure mode most likely to be invisible to the writer**, because they already know
which reading is intended, so the wrong one never occurs to them. It is exactly what a fresh reader
catches and the author cannot, which makes it prime material for pass 2.

Three causes account for most of it in technical prose.

### The dropped "that"

English lets you delete the relativizer, and editors trained on "omit needless words" delete it by
reflex. That's fine until the words after the noun could also be read as the sentence continuing:

> "...from the single decode base generation already holds"

Nothing marks where the noun phrase ends, so the reader takes "the single decode base generation" as
one thing and then hits "already holds" with no subject to attach it to. Restoring one word fixes it:

> "...from the single decode **that** base generation already holds"

The classic examples work the same way: "The horse raced past the barn fell", "The cotton clothing is
made of is grown in Mississippi". **Put "that" back whenever a noun is followed directly by something
that could be read as a verb.** It is one syllable, and it is not padding; it's the signpost that
tells a reader which structure they're in.

The same applies to "that" after a reporting verb: "understand the design of their headquarters
reflects their culture" makes the reader start parsing "the design" as the object of "understand".

### Noun stacks

Nouns in a row, each modifying the next. The reader has no way to know which word is the actual head
noun and which are functioning as adjectives, so they guess, and they guess wrong about as often as
not. The US federal plain-language guidance puts the mechanism well: readers "think they've found the
noun when they're still reading adjectives".

**The working limit: two nouns are usually fine, four is too many, and at three you should check
whether one can go.** Past that the string stops being parseable at all:

> "underground mine worker safety protection procedures development"

The other cost is that a stack compresses several ideas into a space too small to hold them, and the
result is often genuinely ambiguous rather than merely slow. "Sensitive protein function monitoring
system" has no single reading: is it monitoring sensitive proteins, or monitoring protein function
sensitively? No amount of care by the reader recovers the answer, because it isn't in the sentence.

Three fixes, cheapest first:

- **Hyphenate** to show which words bind together. "Data bound control table" becomes "data-bound
  control table", and one character has removed the guesswork.
- **Unpack with prepositions and articles**, which is what those words are for: "developing procedures
  to protect the safety of workers in underground mines".
- **Introduce an abbreviation** where the full term is genuinely standard and will repeat, the way
  "polymerase chain reaction (PCR)" does the work once and then stops.

"Single decode base generation" is the same defect in miniature, and it's why that sentence has two
problems at once rather than one.

### Words that can be more than one part of speech

"Reads", "holds", "processes", "records", "runs", "builds", "returns" are all both nouns and verbs,
and technical vocabulary is unusually full of them. A sentence that opens on one invites the wrong
reading immediately: "Reads base, writes serving" gives the reader no way to tell, at the point they
meet the word, whether "reads" is a verb with an implied subject or a plural noun. Give the verb its
subject, or make the noun plainly a noun.

**The fix is almost never to shorten.** All three repairs add a word: a relativizer, a preposition, an
article, a subject. Say that explicitly in the report, because it runs against the instinct the rest
of this file encourages, and an author who has absorbed "cut words" will otherwise resist it.
Ambiguity costs more than three syllables.

**How to check.** Read the sentence once, quickly, and notice whether you had to back up. That
stumble is the finding. If you're unsure whether a reading is genuinely ambiguous, it is: a sentence
you have to think about to defend has already cost the reader the thing you're defending.

## Dense paragraphs that are really lists

**When a paragraph enumerates, make it enumerate visibly.** A sentence carrying four or five parallel
facts, strung together with commas, semicolons and "and", is a list that hasn't been formatted as
one. The facts are all there and the reader has to hold each one in their head while parsing the next
clause to find out where the boundaries are.

> Its own worker task, a sibling of the pipeline worker, with the same container/ECS-service shape,
> so it can be scaled independently and run to completion rather than sitting in the ingest path. It
> reuses the NetVips core and the ensure-routine; it holds no image logic of its own.

Six facts in two sentences. As a list, each one is a line the eye can land on:

> - Its own worker task, a sibling of the pipeline worker
> - Same container and ECS-service shape
> - Scaled independently
> - Runs to completion, outside the ingest path
> - Reuses the NetVips core and the ensure-routine
> - Holds no image logic of its own

Nothing was cut. The information density is identical; the *parsing* cost isn't. Technical readers
scan bullets and skim paragraphs, so a list is also what makes a fact findable on the second visit.

**Signs a paragraph wants to be a list:**

- Parallel grammatical shapes repeating (three noun phrases, or three clauses all starting with a
  verb).
- Commas doing two jobs at once, separating list items and clauses in the same sentence.
- You have to read it twice to count how many things it mentions.
- The reader would plausibly want to refer back to one item without the others.

**Where it goes wrong:** bullets are not a way to avoid writing sentences. A list of fragments with
no stated relationship between them is worse than a paragraph, because the connective tissue is a
fact too. Keep the prose when the order matters, when each step causes the next, or when the items
aren't actually parallel. Bulleting an argument usually destroys it; bulleting an inventory usually
rescues it.

## Figures of speech and catchphrases

Technical documentation runs dry by default. That isn't a lack of ambition. A reader who came for a
fact is best served by prose that stays out of the way, and a phrase chosen for punch is a phrase not
chosen for accuracy.

The distinction worth making is not vivid versus plain, it's **load-bearing versus incidental**:

- **A figure that explains** earns its place. "The index is a snapshot; the log is the tape." If the
  metaphor is doing work no plain sentence does as compactly, keep it.
- **A named concept** earns its place, and then the name should be used consistently. Backfill,
  fan-out, cold start, circuit breaker, the change test: a coined name is friction the first time and
  shorthand every time after. See [headings are labels](#headings-are-labels-not-descriptions) for
  introducing one.
- **Everything else is incidental.** A phrase from a chat message, a dictated note, or a commit
  message that got promoted into the document and then repeated as a motif. It reads as house style
  to whoever edits next, so it survives every subsequent pass.

**Provenance is not intent.** The author wrote it, so it looks like voice, and a fresh editor defends
it. That's the deference failure in this skill's pass 2, in its most durable form. Someone saying
"then we can scale up resource to crush it" in conversation has not decided that *crush* is the
project's vocabulary. Turning it into a `## Scale to crush` heading is the editor's addition, not the
author's.

Three questions, and one is usually enough:

- **Does the phrase carry a fact a plain word wouldn't?** "Crush it" over "handle the load" adds
  confidence, not information.
- **Would a reader who wasn't in the original conversation know what it means?** This is the stranger
  test, and offhand phrasing fails it most often, because it was shorthand for something the room
  already knew.
- **Would the author use this phrase writing the document cold?** If it only exists because it was
  said once, it isn't voice.

**Headings and names are where this costs the most.** A heading is an index entry, a section link,
and a search target, so a flippant one is wrong in three places at once, and it licenses the same
register throughout the section beneath it. Same for a class or method name: a joke in an identifier
is permanent and gets typed by people who never heard it.

Where you cut one, say which of the three questions it failed rather than calling it informal. The
author can then tell you it was deliberate, which is a real answer you should accept.

## Headings

Headings are navigation. A reader scans them to decide where to go, so a heading's only job is to
name what's underneath it accurately.

| Instead of | Write |
|---|---|
| The one reviewed exception: Cloudflare Turnstile | Exception: Cloudflare Turnstile |
| Why this matters for this project specifically | Why |
| No savings plan, everything on demand, deliberately | On-demand pricing |
| A deep dive into the caching layer | Caching |
| Getting started is easy | Getting started |
| Scale to crush | Scaling |
| Not needed to migrate today's data | Existing images |

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
2. **Turn a clause pile into bullets.** Parallel things in one sentence read better as separate
   lines. Technical readers scan bullets; they don't scan compound sentences. See
   [dense paragraphs that are really lists](#dense-paragraphs-that-are-really-lists).
3. **Delete the sentence.** The most common correct fix.
4. **Replace the abstraction with the concrete fact.** "Improves reliability" → "retries failed
   writes three times".
5. **Give the number.** Any claim about size, speed, or frequency that doesn't have one is weaker
   than it looks.
6. **Rename the heading** to what's under it.
7. **Put back the word that prevents a misreading**: a dropped "that", a preposition inside a noun
   stack, a missing subject. The one move here that adds words. See
   [sentences that mislead on first read](#sentences-that-mislead-on-first-read).
8. **Cut to the audience's level.** Delete the explanation of a concept the actual reader already
   has.
9. **Merge two sentences that say the same thing** in different words. Models often restate a point
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
- **Keep the words that hold a sentence together.** Relativizers, prepositions and articles are not
  padding, and cutting them is how a clean sentence becomes an ambiguous one. Brevity is not the
  goal; the goal is a reader getting the fact on the first pass.
- **Don't flatten voice into a monotone.** The target is how a competent engineer writes when they're
  being clear, not a stripped register with no personality. Plain is about structure and word choice,
  not about draining the text. This protects rhythm and directness; it does not protect a phrase
  purely because the author happened to say it. See
  [figures of speech and catchphrases](#figures-of-speech-and-catchphrases).
- **Don't simplify the content.** Splitting a sentence is good; explaining a concept the audience
  already has is condescending and makes the document longer.
