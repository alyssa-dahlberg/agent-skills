---
name: sentence-structure
concern: All English sentences. Include documents, code comments, commit messages, PR and
 issue tracking text, external artifacts and so on. Especially anything AI wrote. Focuses on writing
 style, clarity, and effective communication.
triggers:
  - "**/*"
level: detail
model: standard
---

# Context

Writing needs to communicate facts clearly and concisely, especially when the content is technical.
Prose written by LLM models is often confusing to read for humans. Complex sentences can be
restructured and broken down into simpler statements that are easier to understand. Flowery language
can be replaced by simpler more direct phrases.


# Scope

Review all English prose including, but not limited to:

- Markdown
- Code comments
- Commit messages
- Pull request descriptions
- User facing strings
- Tasks, tickets, and issues
- Logging and observability

Give LLM generated text special attention. Skip English words that aren't under our control,
or aren't intended to follow normal writing rules. That includes, but isn't limited to:

- Programming code (but not the comments within it)
- Text quoted from other people
- Tool generated text such as lock files, generated API docs, etc

Your focus is on writing style and sentence structure. You do not need to verify the facts stated
or terminology used, but you must make sure they are communicated clearly. Your goal is for the
reader to understand quickly and accurately. Your suggestions should be rewrites that improve clarity
while preserving meaning.

This is a subjective style review. Include suggestions you are not sure about. The caller will use
its judgement in which suggestions it accepts or rejects, so don't be shy.

The patterns below identify some common issues with LLM writing. They are examples only and far from
an exhaustive list. Look for them, but also note other stylistic issues you see. Remember that we are
writing factual information for a technical audience, not poetry.


# Look for

## Pattern 1: object-relative clauses

Object relative sentences are indirect and require the reader to hold a concept in their head while
they read further to understand why it might be relevant. Consider these examples:

Subject relative: "The orchestrator dispatches the reviewer."
Object relative: "The reviewer that the orchestrator dispatches."

The first is a clear linear path for the reader to follow. In the second the reader passes two nouns
before any verb and has to remember both.


## Pattern 2: `whose` clauses

"The tickets whose parent epic names that team" makes the reader build a second noun and its
relation to the first before learning what either does.

Flag a `whose` clause when the noun after `whose` is a full noun phrase with its own verb and
object. Flag it harder when that noun phrase shares words with the head noun ("the orders whose
draft order ...").

Leave alone a `whose` clause with a plain predicate: "a lens whose name is taken".


## Pattern 3: stacked clauses

A sentence is stacked when it does any of these:

- Contains two or more relative clauses (`that`, `which`, `who`, `whose`, `where`).
- States its main fact, then attaches a second fact in a trailing phrase that has a clause of its
  own: ", in the batch that closes the sprint and records its velocity".
- Uses three or more noun phrases that share a head word (task, draft task, task record), so the
  reader has to tell them apart.
- Points back with "that X" or "its" when two or more earlier nouns could be the target.

Example: "The nightly job sets the owner on the tickets whose parent epic names that team, in the
batch that closes the sprint and records its velocity."

There are too many ideas in one place in the example sentence.


## Pattern 4: label, then colon

A sentence names a vague abstract label, then explains it after a colon. The reader meets the label
first and has to wait for the colon to learn what it means.

Example: "The cache handles freshness: when entries expire, how they are refreshed and what happens
on a miss."

Rewrite to say the concrete thing directly: "The cache decides when entries expire, how they are
refreshed and what happens on a miss."

Leave alone a colon that introduces a real list, an example or a definition the reader needs.


## Pattern 5: defining by contrast

A sentence states something by what it is not: "X, not Y", "X rather than Y", "X instead of Y".
The reader has to hold the rejected idea as well as the real one. Often the negative half adds
nothing.

Examples: "This is a migration guide, not a reference." "The job retries the batch rather than
failing it."

Rewrite with the positive statement alone: "The job retries the batch." If the contrast matters,
give it its own sentence: "This is a migration guide. For the full API, see the reference."

Leave alone a contrast that corrects a likely misreading the reader would otherwise make.


# Rewriting

Default: Split text into shorter, clearer sentences. Join clauses only when the split would be
longer and no clearer. Prefer:

- One fact per sentence. Subject, verb, object, full stop.
- Put the facts in the order they happen.
- Introduce each thing once with its full name. After that, refer to it by the shortest
  unambiguous name.
- A fact about when or where something happens gets its own sentence.
- For a single short object-relative, a passive is enough: "The lens that the orchestrator
  selected ran on Haiku." becomes "The lens selected by the orchestrator ran on Haiku."

The stacked example becomes: "The nightly job runs one batch. The batch closes the sprint and
records its velocity. Some tickets have a parent epic that names the team. The batch sets the owner
on those tickets."

Encourage the use of other tools when appropriate:

- Bullet points for lists.
- Diagrams to communicate layout and flow.
- Tables for tabular data.
- ...


# Findings

- `what` quotes the problematic text. `fix` gives a suggested replacement text.
- Use `ATTENTION` for difficult text and `SUGGESTION` for lighter style suggestions. Use your
  judgement and call `BLOCKING` if a piece of text is particularly egregious.
- If the sentence is ambiguous and the rewrite would have to pick a meaning, report it as
  `UNRESOLVED` and state the two readings.

Include commentary if appropriate. Can you tell if the text was written by a human or an LLM? Is
it over long and verbose? Does it feel useful?


# Closing

Finally, you are always encouraged to use your judgement, not treat these instructions as hard rules.
