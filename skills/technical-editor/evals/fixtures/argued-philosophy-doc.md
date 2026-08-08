# Abstraction Altitude

Every piece of writing — code or prose — is written from somewhere. A function might describe *what* a checkout flow does, or it might describe *how* bytes get flushed to a socket. A design doc might explain why we're migrating a service, or it might list the environment variables the new deployment needs. Neither position is wrong. What is wrong is occupying both at once, in the same body of text, without telling the reader you've moved.

We call this **abstraction altitude**: the height above the machine at which a given piece of writing sits. A well-formed function, paragraph, or module holds a steady altitude. A poorly formed one climbs and dives, and the reader has to pay to follow.

## Why it matters

The cost is cognitive, and it is paid on every read.

When you read code, you build a model of what it does. If a function is written at a consistent altitude, that model is cheap to build: you read five lines that are all about the same kind of thing, and you understand the shape of the whole without needing the parts. `validate(order); reserve(inventory); charge(payment); confirm(order)` tells you the story of checkout in one glance. You can stop there and still be correct about what happens.

Now drop one altitude change into the middle:

```
validate(order);
reserve(inventory);
const idempotencyKey = crypto.createHash('sha256')
  .update(`${order.id}:${order.version}:${Date.now() / 60000 | 0}`)
  .digest('hex');
charge(payment, idempotencyKey);
confirm(order);
```

The story is still there, but you can no longer skim it. Those three lines force you down to the level of hash functions and minute-bucketed timestamps, and having gone down, you have to climb back up to resume the narrative. Worse, their presence implies significance. A reader reasonably assumes that anything written at a lower altitude than its neighbours is there because it *had* to be — that the detail matters to understanding the whole. Usually it doesn't. Usually it's just where the author happened to be standing when they wrote it.

This is the real damage. Mixed altitude doesn't only cost attention; it costs *trust in the text*. Readers stop being able to tell which details are load-bearing.

The same holds for documents. A migration plan that spends four sections on strategy and then, in section five, inlines the exact `ALTER TABLE` statement, has told its reader that this statement is somehow more important than the hundred other statements the migration will run. Maybe it is. But if it isn't — if it's there because the author had the SQL open in another window — the document has quietly lied.

## How it shows up

A few patterns we see repeatedly:

**The one deep line.** A function of clean, well-named calls, with one raw expression buried in it. Almost always this wants to be extracted and named, not because the expression is long but because naming it restores the altitude.

**The helper that isn't.** A function called `processOrder` that both orchestrates the high-level steps *and* contains the retry loop, the logging, and the error mapping. It reads as one thing but is three things at different heights.

**Prose that drops into implementation.** A design doc explaining a system, which suddenly starts naming classes. Class names are an implementation altitude. If the doc is about the design, they belong in an appendix or a linked file.

**Prose that never lands.** The inverse, and just as common. A document that stays so high that it never says anything falsifiable — "we will improve reliability through better observability" — is holding altitude, but at a height where nothing is visible. Consistency is not the goal in itself. The goal is to pick the altitude the reader needs and *stay there*.

**The README that's four documents.** Overview, install steps, API reference, and architecture notes interleaved. Each is fine. Braided together, none of them is readable.

## How we think about it

Three habits.

**Name the altitude before you write.** Ask: who is reading this, and what do they need to be able to do afterwards? A runbook is written at operational altitude — commands, paths, exact strings. An architecture doc is written at systems altitude — components, boundaries, data flow. Deciding this first is most of the work; the writing tends to follow.

**When you find yourself descending, extract.** In code this means a named function. In prose it means a linked document, a footnote, or an appendix. The instinct to extract shouldn't come from length — a three-line function is fine if those three lines are one altitude below their caller. It should come from noticing that you've changed heights.

**Make transitions explicit when you do need them.** Sometimes a document genuinely has to move between levels. That's fine, as long as it's announced: a heading, a section break, a sentence that says "concretely, this means". What breaks the reader is the *unmarked* transition — the drop they don't see coming.

None of this is a rule we enforce mechanically. There's no linter for it, and we're wary of the version of this idea that turns into dogmatic one-line functions or documents so layered that nothing is ever said. It's a lens, not a law.

But it's one of the highest-leverage lenses we have, because it applies to everything we produce and it compounds. Code that holds altitude is code you can skim, which means it's code you can review honestly, which means it's code that stays correct. Documents that hold altitude are documents people actually finish.

When something you've written feels hard to read and you can't say why, this is the first thing to check.
