# Detection spec

**What this skill is expected to catch, not instructions for catching it.** Nothing here is loaded at
runtime. It exists so that changes to the skill can be tested against a stable list of what good
output looks like, and so the reasoning behind the list isn't lost.

## Why this isn't in the skill

These patterns were originally written as a catalogue the editor read while working. Three
independent tests said that didn't help:

| Test | Result |
|---|---|
| Same fixture, skill with the catalogue vs skill without | Identical findings, including every prose tell |
| Same fixture, no skill at all | Caught every seeded tell unaided |
| A sweep with the catalogue, run after a pass without it | Nothing new, on four candidates examined and reasoned about |

**As of August 2026, the models this skill targets (Opus 5 and Haiku 4.5 in these runs) recognise
these patterns without being shown a list.** What they lacked, and what the skill supplies, is the
placement and verification work: which artifact owns a fact, whether a documented value survives its
config overrides, how long a document is meant to last.

So this is a record, not a rule set. It's here for three jobs:

- **Eval coverage.** Every entry should be exercised by a fixture, or knowingly not. See the coverage
  table below.
- **Regression detection.** If a future model stops catching something here, that is a signal to put
  the guidance back, and this file is what to put back.
- **Design memory.** So the next person doesn't rediscover the list, add it to the skill, and repeat
  the experiment.
- **Prompting a consulted model.** If you ask a model from another family for a second opinion on
  prose, naming the specific tells you care about gets a much sharper answer than "review this for
  clarity", and this is the list to paste in. That isn't the anchoring problem returning: anchoring
  is about a reviewer narrowing its own independent reading, and a targeted second opinion is a
  different job with a question already attached.

If you are editing the skill and reaching for something here, check the coverage table first: the
question is whether current models still handle it, and that is measurable.

## Coverage by fixture

Honest state, not aspiration. Eleven of the thirty-two below are unexercised.

| Pattern | Fixture |
|---|---|
| Manufactured antithesis | `doc-code-drift-repo`, `inflated-commit-message` |
| Marketing / clickbait heading | `doc-code-drift-repo` |
| Throat-clearing opener | `doc-code-drift-repo` |
| Inflated verb | `doc-code-drift-repo` |
| Style word ("seamless", "robust") | `doc-code-drift-repo` |
| Self-justification ("deliberately") | `doc-code-drift-repo`, `inflated-commit-message` |
| Vague declarative | `doc-code-drift-repo` |
| Emphasis crutch ("fundamentally") | `inflated-commit-message`, `backfill-design-excerpt` ("at all") |
| Dash-and-elaborate | `argued-philosophy-doc` |
| Aphoristic closer | `argued-philosophy-doc` |
| Counting what you're about to list | `argued-philosophy-doc` |
| Restating the container | `argued-philosophy-doc` |
| Rule-of-three | `argued-philosophy-doc`, `out-of-scope-fiction` (as a **must not flag**) |
| Overloaded sentence | `spec-derived-architecture-doc` (lightly), `backfill-design-excerpt` (four facts, one sentence) |
| **Uniform cadence** | none |
| **Transition stacking** | none |
| **Fake authority** | none |
| **Summary bookends** | none |
| **Trailing coda** | none |
| **Passive hiding the actor** | none |
| **Dramatic fragmentation** | `backfill-design-excerpt` ("This design is that worker.") |
| **Nominalisation** | none |
| **Intensified adjective** | `backfill-design-excerpt` ("first-class", "defensible at all") |
| **Borrowed term of art** ("anaphora", "ratify") | none |
| **Latinate formality** ("commence", "obviate") | none |
| **Definite-article heading** | none |
| **Heading describing rather than naming** | `backfill-design-excerpt` ("Not needed to migrate today's data") |
| **Offhand phrasing promoted to vocabulary** | none |
| **Thinking left in** (derivation not conclusion) | `backfill-design-excerpt` |
| **Garden path / dropped relativizer** | `backfill-design-excerpt` |
| **Noun stack** | `backfill-design-excerpt` |
| **Paragraph that should be a list** | `backfill-design-excerpt` |

The gaps aren't evenly important. The word-level ones are cheap to add to an existing fixture and
would firm up the "models handle this unaided" claim, which currently rests on the patterns that
happen to be seeded. The structural ones, uniform cadence especially, are harder to seed
convincingly, since they only exist at document scale.

`measure.py` covers a few of these mechanically (style words, inflated verbs, borrowed terms,
Latinate formality, em-dash density, burstiness), which is not the same as testing whether the skill
*reports* them usefully.

---

The rest of this file is the pattern list itself. Every entry is the right choice in some sentence
somewhere; a finding is only a finding if you can say what it costs this reader in this sentence.

## Structural patterns

**Manufactured antithesis.** "This isn't just a refactor — it's a rearchitecture." "Not X. Y." The
frame implies a contrast the reader never proposed, and the negated half is filler. State the
positive half.

**Rule-of-three lists.** "Efficient, scalable, and reliable." Three adjectives arrive together
because the rhythm is satisfying, not because there are exactly three relevant properties. Keep the
ones that are load-bearing facts; usually that's one, sometimes zero.

**Consequence tacked onto a fact.** "The worker is a separate ECS service, so this is a displacement,
not a rewrite." The fact is the first clause. The second is reassurance, and it's the author arguing
with an objection the reader hasn't made. If the consequence genuinely matters, make it its own
sentence and make it specific: "It can be moved later."

**Self-justification.** "No savings plan — everything on demand, deliberately." "This is an
intentional design choice." We wouldn't be documenting it if it were an accident. Cut the defence; if
there's a real reason, give the reason instead.

**Restating the container.** Text repeating something its position already established. A heading, a
list, a table column, a section, a file's location, a type's name. Each sets a context that
everything inside inherits for free. Repeating it costs the reader a word every time and adds
nothing.

| Container | Written | Should be |
|---|---|---|
| A list under "Placement tests" | "The change test. If this fact changed tomorrow..." | "Change. If this fact changed tomorrow..." |
| `## Installation` | "To install the package, run..." | "Run..." |
| `## Troubleshooting` | "### Troubleshooting slow queries" | "### Slow queries" |
| A "Description" table column | "This option controls the timeout" | "Controls the timeout" |
| A doc comment on `Order.Total` | "The total of the order." | delete it |
| A file in `src/Worker/` | "The worker module handles..." | "Handles..." |
| `enum OrderStatus` | `OrderPending`, `OrderShipped` | `Pending`, `Shipped` |

The general move: read what's above and around the text, then delete whatever the reader has already
been told by getting there. It applies identically to prose and to names: `OrderService.ProcessOrder(Order order)`
is the same defect as a bullet repeating its own heading. See
[code as communication](../reference/information-architecture.md#code-as-communication).

Some limits. Enough context must survive that the fragment still parses on its own, because readers
arrive mid-document from links and search. And a term repeated for genuine disambiguation, where two
similar things are in play, is doing work, and cutting it there costs clarity rather than saving words.

**Counting what you're about to list.** "There are five things to check:" followed by five bullets.
"The pipeline has four stages:" above a four-row table. The reader can see how many there are, so the
number tells them nothing, and it's now a second fact to maintain. Add a sixth item and the sentence
is wrong, with nothing to catch it.

> **Now:** The scanning worker performs three checks:
>
> **Suggested:** The scanning worker performs these checks:

This is the [enumeration problem](../reference/information-architecture.md#listing-values-that-change) at sentence
scale, and it's how counts drift out of step with their own examples: "you read five lines" above a
four-line snippet, "our three regions" beside a list of four. When you find a count next to a list,
check it before deciding what to do with it; a wrong one is a real finding, not a style note.

The same applies to counts in prose describing something visible elsewhere: "the four buckets", "both
workers", "the three-step process". These are fine while true and silently wrong afterwards. Name the
things or point at them.

Keep the count when it's doing work the list can't:

- The list is long or paginated and the reader needs the scope before committing to it.
- The number is the point: "all three replicas failed", "only one of the five is required".
- It's a completeness claim the reader should check you on: "the four cases below are exhaustive".

**Throat-clearing openers.** "Here's the thing:", "It's worth noting that", "Let's dig into", "In
today's landscape". Delete and start at the fact.

**Summary bookends.** An intro paragraph that previews the section and a closing paragraph that
recaps it. In a short document both are re-reading. Keep them only when the section is long enough
that a reader might land in the middle of it.

**Uniform cadence.** Sentence after sentence of similar length and shape. Human writing is bumpy:
a long explanatory sentence, then a short one. If everything is 20 words, the reader's eye stops
finding purchase. Fixing this usually means merging some sentences and cutting others, not padding.

**Transition stacking.** "Furthermore", "Moreover", "Additionally", "Ultimately" opening consecutive
paragraphs. If the order of ideas is right, most transitions are unnecessary.

**Fake authority.** "Studies show", "it's widely accepted", "best practice dictates" with nothing
behind it. In a codebase, either link the source or state it as your team's decision.

## Sentence-level patterns

**The overloaded sentence.** One sentence carrying two or three ideas, joined by whatever punctuation
is to hand: em dashes, parentheses, commas, colons, semicolons. The connector varies; the habit is
the same, and it's the highest-yield fix in most AI-written technical prose.

> "The worker (which runs as a separate ECS service, unlike the API) polls the queue every 30
> seconds — this is configurable — and writes results to the store, though failures go to a DLQ."

Nothing there is wrong. It's just four facts in one sentence, so the reader has to hold three of them
open while parsing the fourth. Split it:

> The worker runs as a separate ECS service. It polls the queue every 30 seconds (configurable) and
> writes results to the store. Failures go to a dead-letter queue.

**Default to splitting.** Two plain sentences almost always beat one sentence with a subordinate
clause bolted on. Ask what each connector is doing:

- **Parentheses**: if the aside matters, it's a sentence; if it doesn't, delete it. The exception is
  a genuinely brief gloss like a unit or an example.
- **Em dash**: usually joining two facts, or introducing a restatement (see
  **Dash-and-elaborate**, next in this section). Both split cleanly. **Look at every one**: this mark
  is the exception to the density rule, because it's the most overrepresented in machine prose and it
  spreads to people who read a lot of it. Ask what relation it's hiding and use punctuation that says
  so; a comma in its place is not a fix. Corpus averages don't acquit an individual dash, since they
  include writing where it's a deliberate instrument. See
  [em dashes](../reference/plain-language.md#em-dashes).
- **Colon**: earns its place introducing a list or a definition. Used for a dramatic reveal, it's
  doing rhetoric.
- **Semicolon**: fine between two genuinely balanced clauses, but usually a full stop wants the job.
- **Comma splices and trailing "which" clauses**: the commonest form, and the easiest to miss
  because it reads smoothly.

The limit is that splitting can destroy real connective tissue. If two clauses are causally linked,
keep the link and make it explicit with a word ("so", "because", "which means") rather than leaving
the reader to infer it from punctuation. Three consecutive four-word sentences is its own problem;
you're aiming for one idea per sentence, not one clause.

> "This also subsumes the old lambda reserved concurrency concern — a single worker with a bounded DB
> pool caps RDS connections by construction."

Two facts welded together, and the second only parses if you already know the story. Rewrite as
statements, or as bullets:

> The worker holds a bounded DB pool, so RDS connections are capped by the pool size. This replaces
> the old Lambda reserved-concurrency limit.

**Dash-and-elaborate.** Distinct from the overloaded sentence, and more common. A claim, then a dash, then a
restatement of the same claim in more balanced or rhythmic words. No new fact arrives after the dash.

> "A fact written in three places is three things to maintain, and in practice they diverge — the
> code changes, one copy gets updated, and now the repo contradicts itself."
>
> "These patterns are symptoms of writing that isn't committing to anything, and the fix — say the
> concrete thing — is what actually helps the reader."

The tail sounds like the sentence arriving somewhere, which is why it's easy to write and satisfying
to leave in. It's more reliable than any word list, because it's a rhythm rather than a
vocabulary.

The fix is almost mechanical: cut at the dash and make both halves sentences, then delete whichever
one is redundant. Often the tail was the real content and the opening clause was throat-clearing.

> "A fact written in three places is three things to maintain. In practice they diverge: the code
> changes, one copy gets updated, and the other two are now wrong."

**Aphoristic closers.** A short, balanced sentence at the end of a paragraph that restates what the
paragraph just said, in a form that sounds quotable. "Keep the facts, lose the packaging." "That's
the difference." "The rest is detail." They feel like landing the point; they're re-reading. Delete
them, because the paragraph already made the point, and if it didn't, the closer won't rescue it.

**Trailing codas.** The same instinct at sentence scale: a clause tacked on with "and" that comments
on what was just said rather than adding to it. "...duplicated explanations are usually near-verbatim,
and that's how you find them." "...is noise, and the author will start ignoring you." Sometimes the
coda is the only real content; keep that half and cut the setup.

**Sentences that assume unshared context.** The stranger test: would a competent reader who wasn't in
the design conversation follow this? Text referring to "the old concern", "the previous approach", or
"as discussed" without establishing them fails. Either establish the context in one clause or cut the
reference.

**Hedging that never commits.** "This might potentially help reduce", "can serve to improve", "should
generally be considered". Either it does or it doesn't; if it's genuinely conditional, name the
condition. "Under load above ~200 rps this reduces p99 latency" is useful. "This may improve
performance" is not.

**Passive voice hiding the actor.** "The connection is closed", by whom and when? In technical prose
the actor is usually the interesting part.

**Vague declaratives.** Sentences that sound like information and contain none: "The key is
balance." "This gives us flexibility going forward." Apply the deletion test; they never survive it.

**Dramatic fragmentation.** "Every request. Every time." Fine once in a blog post, out of place in
documentation.

## Word-level patterns

**Inflated verbs.** Swap for the plain word.

| Inflated | Plain |
|---|---|
| utilize, leverage | use |
| facilitate, enable | help, let, allow |
| implement (of a decision) | do, make |
| surface, expose (of information) | show |
| navigate | handle |
| orchestrate (of two things) | run, coordinate |

**Words that send the reader to a dictionary.** The bar is not "an educated reader could look this
up". It's that nobody should need to. A reader who stops to check a word has lost the thread of the
sentence, and if they guess instead they may guess wrong.

Two kinds, and they need different handling.

**Terms of art borrowed from another field.** Precise, correct, and useless to this audience: the
writer knows a word from rhetoric, law, or linguistics and reaches for it in a software document.

| Borrowed | Say |
|---|---|
| anaphora | the repeated opening, or just quote it |
| ratify | decide, agree, approve |
| taxonomy (of a list of options) | the categories |
| orthogonal (of unrelated things) | unrelated, independent |
| a priori / prima facie | in advance / at first glance |
| dialectic, teleology, epistemic | almost always the wrong register entirely |

The test is whether it's a term of art **in the reader's field**, not in some field. `idempotent`,
`tsvector`, `merge-base` and `backpressure` all stay. They're precise, standard, and a working
engineer knows them or needs to. `anaphora` goes, because a working engineer has no reason to know it
and the plain phrase costs nothing.

**Latinate formality where a plain word exists.** The register lifts without the meaning changing.

| Formal | Plain |
|---|---|
| commence, initiate | start |
| ascertain, determine | find out, work out |
| prior to / subsequent to | before / after |
| endeavour, attempt | try |
| requisite, requisite for | needed, needs |
| obviate | avoid, remove the need for |
| ameliorate | improve |
| aforementioned | the, this, that |
| in the event that | if |
| a myriad of | many |
| notwithstanding | despite, even so |

**Write for readers whose first language isn't English.** Many of your readers are reading a second
or third language, often very well, and the gap is rarely technical vocabulary, since they read specs and
code all day. It's the literary and Latinate layer: the idioms, the borrowed rhetoric terms, the
formal register that carries a social signal rather than a fact. That layer is exactly what carries
no information anyway, which is why cutting it costs nothing and helps a lot.

Idioms and cultural references have the same problem: "the elephant in the room", "moving the
goalposts", "boil the ocean", "gotcha", sports and war metaphors. Fine in conversation, avoidable in
a document that will be read across time zones.

**Offhand phrasing promoted to vocabulary.** A phrase from a conversation, a dictated note, or a
commit message reused as a heading or a repeated motif ("scale to crush", "make it sing", "the
nuclear option") where a plain label would do. It reads as the author's voice, so editors preserve
it, but it usually got there because someone said it once. A metaphor that explains something and a
named concept (backfill, cold start, circuit breaker) are different and should stay.

**Reaching for the fancy word usually means the sentence is performing.** It's the same diagnosis as
everything else here: the register is doing work the content should be doing. When you flag one,
check whether the sentence around it is also saying less than it appears to.

**Style words.** Overrepresented in model output and rarely carrying a fact: *delve, tapestry,
landscape, realm, seamless, robust, crucial, pivotal, underscore, showcase, comprehensive, holistic,
myriad, testament*. Ask what each is claiming. "Robust error handling" claims nothing; "retries three
times with backoff, then dead-letters" is the fact.

**Emphasis crutches.** *genuinely, fundamentally, truly, actually, simply, at its core, load-bearing,
critically*. These add insistence, not information. Almost always deletable without loss.

**Intensified adjectives.** "Extremely important", "highly optimised", "significantly faster".
Either give the number or drop the intensifier.

**Garden-path sentences and miscues.** Grammatical prose that sends the reader down the wrong parse,
so they reach the end and have to go back. Three causes dominate in technical writing.

- **A dropped relativizer.** "The single decode base generation already holds" reads as one long noun
  phrase until "already holds" arrives with no subject. Put "that" back. Same after reporting verbs:
  "understand the design of their headquarters reflects their culture".
- **Noun stacks.** Nouns in a row, each modifying the next, with nothing marking the head. Readers
  "think they've found the noun when they're still reading adjectives". Two is usually fine, three
  wants checking, four is unreadable. Fix by hyphenating, unpacking with prepositions, or abbreviating.
- **Words that are both noun and verb** at the point the reader meets them: *reads, holds, records,
  runs, processes, returns*. Give the verb its subject.

The repair adds a word rather than cutting one, which is why an editor optimising for brevity
introduces these. Say so when reporting, or the suggestion reads as padding.

**A paragraph that is really a list.** Four or more parallel facts joined by commas and semicolons,
where the commas are separating list items and clauses at the same time. Nothing is wrong with the
words; the reader is paying to find the boundaries and cannot refer back to one item later. Bullet
it, cutting nothing. The limit is that bullets destroy an argument, whose connective tissue is itself
a fact, while rescuing an inventory.

**Nominalisation.** "Perform a validation of" → "validate". "Provides support for" → "supports".
"Make a determination" → "decide". Verbs read faster than noun phrases built around them.
