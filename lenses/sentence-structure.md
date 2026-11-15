---
name: sentence-structure
concern: English sentences, wherever they appear (docs, comments, commit messages, PR and issue text, pasted Notion or Jira content), are built so a reader parses them once, each carrying one fact, without holding nouns in mind while waiting for a verb.
triggers:
  - "**/*"
level: detail
model: standard   # judging which sentences are hard and writing the replacement is a writing task
---

**Context.** Alyssa reads fast and will not re-read. Most of the prose under review was written by
a large language model, and those models pack several facts into one grammatical but slow sentence.
This lens finds those sentences and supplies short ones: one fact each, ended with a full stop,
close to bullet-point style.

**Scope.**

- Review English prose only: markdown, code comments, docstrings, commit messages, user-facing
  strings, pasted ticket or page text.
- Skip code, identifiers, config values, log output and quoted text from other people.
- For a diff, review added and changed lines only.
- Report only the patterns listed below. Other writing problems belong to other lenses: put them
  in `HANDOFFS:`.
- Meaning, facts and terminology are out of scope. A rewrite changes the structure and nothing else.

## Pattern 1: object-relative clauses

In a subject-relative clause, the noun does the action: "the orchestrator that dispatches the
reviewer". In an object-relative clause, the noun receives it: "the reviewer that the orchestrator
dispatches". The reader meets two nouns before any verb and has to hold both.

Flag an object-relative clause when any of these holds:

- Both nouns are full noun phrases of a similar kind (two components, two people, two documents).
- The clause is nested inside another relative clause.
- More than about five words separate the head noun from the verb that governs it.
- The clause sits between a main-clause subject and its verb, so the main verb arrives late.

Leave it alone when:

- The inner subject is a pronoun or a short name: "the file you opened", "the branch Alyssa pushed".
- The clause is two or three words and ends the sentence: "the model the lens sets".

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

## Rewriting

Default: split into short sentences. Join clauses only when the split would be longer and no
clearer.

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

## Findings

- One finding per sentence, naming the pattern. `what` quotes the sentence. `fix` gives the full
  replacement text.
- Severity: `ATTENTION` for nested object-relatives and stacked sentences. `SUGGESTION` for
  everything else. Never `BLOCKING`.
- If the sentence is ambiguous and the rewrite would have to pick a meaning, report it as
  `UNRESOLVED` and state the two readings.
- Clean prose is the normal result. Say "No findings" and stop.
