---
name: docs-and-comments
concern: Prose docs and code comments carry only non-obvious information, sit at the right abstraction altitude, and stay in step with the code.
triggers:
  - "**/*"
level: detail
model: standard   # judging altitude and restating-the-code needs some reading, not deep reasoning
---

> **This is an example lens**, self-contained and intentionally **broad-triggered** (it applies to
> almost any diff, so it fires on everything and relies on the reviewer's judgement to engage only when
> there's prose or comments worth reviewing). The *Context* is invented — replace it with how your team
> actually thinks about docs.

**Context.** We've lost real time to comments that get out of hand — so our stance is that **a comment
is a cost, not a free good.** The default is *no comment*; a comment has to earn its place by saying
something the code and the docs can't. We especially dislike two habits: comments that **restate a
convention** already written down elsewhere (they go stale and lie), and docs that talk at the **wrong
altitude** — an interface's doc describing its callers or a specific implementation instead of its own
contract. We'd rather read five words that tell us *why* than a paragraph that re-narrates the code.

**Look for the following — a *floor, not a gate*.** The first two are the habits that cost us most;
also flag anything else where prose, comments, or diagrams mislead or drift from the code.

- **Comments that restate the code or a documented convention.** A comment earns its place only by
  stating something the code and docs *don't* — a hidden constraint, a subtle invariant, a non-obvious
  reason, an external workaround. Apply the test: *if deleting the comment loses no non-obvious
  information, delete it.* A comment re-listing validation the constructor already enforces, or
  restating a rule that lives in a style guide, is noise — flag it.
- **Wrong abstraction altitude.** A doc/comment should hold **one coherent horizontal slice** of
  abstraction. Apply the test: *could this sentence only be written by someone looking **up** at my
  callers or **down** at a specific collaborator?* If so it's at the wrong altitude — cut it, or move it
  to the collaborator's own doc / the composition root. An **interface** states the contract an
  implementor guarantees and how a caller uses it — **not** which adapter implements it, not the callers
  by name, not the transport two hops downstream. An adapter talks about its own mapping; a service
  about its own behaviour.
- **Doc lag as a bug.** A code change that should have updated a doc, comment, or diagram and didn't —
  the description now contradicts the behaviour. A contradiction between comment and code, or between
  two docs, is a finding.
- **Prose written as a fact-list rather than for a reader**; duplicating what the code/config already
  shows instead of linking to it; broken cross-links and headings; a false claim in a security/privacy
  statement (treat as blocking).
- **Diagrams** present where they'd carry more than prose (topology, flows, state machines), accurate
  and consistent with the text and code — or drifted from what they depict.
- **Housekeeping.** Commented-out code left in; obvious spelling/grammar errors in shipped prose or
  public API docs.
