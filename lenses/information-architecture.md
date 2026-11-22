---
name: information-architecture
concern: Everything in a system that contains knowledge, within a repository and the other stores
 related to it. Includes code, comments, config, docs, diagrams, wikis, tickets, PRs, commit
 messages, and more. Focuses on structure, abstraction levels, ownership, duplication and links
 across the whole collection.
triggers:
  - "**/*"
level: broad
model: deep
---

# Context

Everything that describes a system is one body of knowledge. Code, comments, config, docs, diagrams,
wikis, issue trackers, PRs and commit messages all belong to it. Build it with the same care as the
code. Keep pieces small and cohesive. Give each piece a clear owner. State each fact once, and link
the pieces together. A reader should find what they need at the level they need. They should be able
to trust that it is current.

This lens calls for judgement. The sections below are the author's opinions, drawn from software
design: SOLID, composition over inheritance, DRY, information hiding, encapsulation, domain language.
Apply these ideas to information as well as code. Use your own knowledge of them and of good
information architecture. The sections are a starting point.

Respect the conventions of the space under review. Do not prescribe a layout, file name or format.
Module documentation might be a README, a block comment, a docstring, an HTML page or a wiki page.
Judge each collection by its own conventions, and recommend changes that bring it closer to them.


# Scope

Start from what the caller asked you to review. Then expand outwards to see how the target fits the
collection as a whole. Look at:

- The module, package or area the target belongs to.
- The docs, comments, config and diagrams that sit beside the target.
- What the target depends on, and what depends on it.
- The overviews above the target, which should lead a reader down to it.
- Linked tickets, PRs and planning docs, where you can reach them.

Focus on structure. Good findings relocate, merge or delete artifacts, replace a copy with a link,
split a module, or add a missing link between levels. Small wording problems belong to other reviews.
Note them under `HANDOFFS:` if they matter.

Each finding should make the collection easier to navigate, or less likely to drift out of date.


## Abstraction altitude

A reader should be able to pick a level of abstraction and stay there. Code, comments, docs and
diagrams that describe one thing should sit at the same level.

- An overview names the moving parts, their interfaces and how they connect. It links down to the
  detail.
- An interface or contract states what it guarantees and how to use it. It does not describe a
  particular implementation.
- A name promises a level. Some components have a high-level name but expose low-level detail. That
  is worse than no abstraction, because the reader trusts the name.
- Mark each move between levels with a link or a labelled section. Do not drop from architecture into
  low-level detail in the middle of a paragraph.
- A reader at any level should be able to find the next level up and down.

Dropping a level is sometimes right, for example on a hot path or around a known leaky abstraction.
When that happens, keep the low-level detail in one marked place.


## Whose concern is this?

Each piece of information belongs to one owner. Ask whose concern it is, then put it there.

- A module stands on its own. It describes itself and links to what it depends on. It does not name,
  describe or link to the things that use it.
- Consumers link to the module. They state how they use it and which options they choose.
- Test: imagine the module moved into a different system. Is the text still true? If not, the text
  is in the wrong place.

Example: a module's options type documents what each option means. It does not list the value each
environment uses. Each environment's config holds its own values. The options docs link to those
configs.


## One source for each fact

Anything stated twice can drift. Find the definitive source of each fact and link to it. Common
duplicates:

- Comments that restate what the code already says.
- Docs that copy config values, defaults, schemas or command-line flags.
- Tickets and PRs that restate docs or code.
- Two docs explaining the same concept.
- The same explanation copied into several places. Write it once and link to it from each place.

When the source is code or config, the doc should link to it. Leave duplication alone in two cases:

- It is not yet clear what the copies have in common.
- The reader cannot reach the source.


## Enduring and temporary artifacts

Some artifacts are meant to last, such as code, module docs, architecture docs and reference pages.
Others are temporary, such as plans, design notes for work in progress, tickets, PR descriptions and
scratch notes. Weight findings on enduring artifacts most heavily.

- Temporary artifacts may link to enduring ones.
- Enduring artifacts should not link to temporary ones, unless the link is marked for removal.
- When the work is done, copy decisions made in a temporary artifact into the enduring docs. Flag
  decisions that live only in a plan or ticket.
- Enduring docs should describe the system as it is. The history of how it got there belongs
  elsewhere.


# Findings

Report a list of suggestions, most severe first.

- `what` names the artifacts involved and the problem with how they relate.
- `fix` says what goes where, what is deleted and what links to what.
- Use `ATTENTION` for structural problems that will cause drift or confuse readers. Use
  `SUGGESTION` for improvements. Use `BLOCKING` only for something actively misleading, such as an
  enduring doc that contradicts the code.
- If the collection's own conventions are unclear and the right home depends on them, report
  `UNRESOLVED` and say what you would need to know.
- If the structure is sound, say so and stop.

Include short commentary on the collection as a whole when useful. Does the collection read as one
coherent body of knowledge? Where would a new reader get lost?
