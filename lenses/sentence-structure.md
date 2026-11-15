---
name: sentence-structure
concern: English sentences, wherever they appear (docs, comments, commit messages, PR and issue text, pasted Notion or Jira content), are built so a reader parses them once, without holding nouns in mind while waiting for a verb.
triggers:
  - "**/*"
level: detail
model: standard   # judging which sentences are hard and writing the replacement is a writing task
---

**Context.** Alyssa reads fast and will not re-read. Most of the prose under review was written by
a large language model, and those models favour indirect sentence structures that are grammatical
but slow to parse. This lens finds those structures and supplies the direct version.

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
- The direct version would be longer and no clearer.

Rewrite with the first of these that reads naturally:

1. Make the doer the subject of a main clause. "The reviewer that the orchestrator dispatches reads
   the lens." becomes "The orchestrator dispatches a reviewer, which reads the lens."
2. Split into two sentences, one fact each. "The token that the gateway that the client calls
   validates expires hourly." becomes "The client calls the gateway. The gateway validates the
   token, which expires hourly."
3. Keep the receiver as the topic with a short passive. "The lens that the orchestrator selected
   ran on Haiku." becomes "The lens selected by the orchestrator ran on Haiku."

## Findings

- One finding per sentence. `what` quotes the sentence. `fix` gives the full rewritten sentence.
- Severity: `ATTENTION` for nested clauses. `SUGGESTION` for everything else. Never `BLOCKING`.
- If no rewrite keeps the meaning exactly, do not report the sentence.
- Clean prose is the normal result. Say "No findings" and stop.
