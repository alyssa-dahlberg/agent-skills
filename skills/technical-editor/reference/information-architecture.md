# Information architecture

How to decide where a fact belongs, and how a reader is meant to find it.

## Levels of detail

Every piece of writing sits somewhere on a scale from "what is this whole system" to "why is this one
line like that". A reader arrives with a question pitched at one point on that scale, and wants an
answer pitched at the same point. Answer at the wrong level and they either drown in detail they
didn't ask for or get a generality that doesn't help.

The scale runs roughly:

**Whole system** → **how the major pieces fit** → **what one component is for** → **the contract of a
type** → **the contract of one member** → **why this specific code is written this way**

Elsewhere this skill calls a text's position on that scale its **altitude**, purely as shorthand.
High altitude means zoomed out: shape, purpose, how things relate. Low altitude means zoomed in:
mechanism, constraints, the specific reason for a specific line. It's a useful word because "level"
is overloaded in software, but it isn't a term of art and you don't need to use it in reports —
say "this is too detailed for a document about the whole system" and any reader will follow.

**What sits at each level is a property of the repo, not of this document.** Where the writing lives
— which files, which folders, which comment conventions — differs by language, framework, team, and
tooling, and this skill has no business assuming. Find out what this repo does before judging
anything. See [learn the repo's conventions](#learn-the-repos-conventions) below.

These rules hold whatever the layout:

**One artifact answers questions from one level.** When a component overview starts explaining a
retry loop's backoff arithmetic, the reader has to change zoom mid-paragraph, and that's the
cognitive overhead we're removing. The detail isn't wrong, it's misplaced — it belongs next to the
code it describes.

**A contract describes the contract, at its own level.** Documentation attached to an abstraction
says what a caller can rely on and what an implementer must provide. It does not reach down into how
any particular implementation works — see [leaky abstractions](#leaky-abstractions-in-prose).

And these follow from them:

**Inline comments explain why, never what.** `// increment the counter` above `counter++` is noise.
`// the API rejects a batch of 0, so we skip the empty case rather than short-circuit later` is a
fact the code cannot carry.

**Nothing describes what is already self-evident.** If a competent reader gets the fact from the
name, the signature, or the two lines below, the prose is a maintenance liability with no upside.
Delete it.

## Progressive disclosure

The levels above describe how far to zoom. This describes when to reveal — and it's the same
instinct, applied to a reader's path through a document rather than to which artifact they're in.

**Say what most readers need, then point to the rest.** Detail that only some readers want doesn't
belong inline, where everyone pays for it; it belongs one link away, clearly signposted, so the people
who need it can find it and the people who don't can move on. A document that front-loads everything
it knows is unreadable at every level of expertise at once.

What this looks like in practice:

- The main path states the principle and links to the depth. "Retries use exponential backoff — see
  `retry-policy.md` for the schedule and the jitter calculation."
- Reference material lives in its own file, not in a long section the reader has to scroll past.
- Long documents put the thing most readers came for near the top and the exhaustive material below
  it, so the document is useful without being read to the end.
- A link is a promise. Signpost what's behind it well enough that a reader can decide *not* to follow
  it — "see X for the full parameter list" tells them more than "see X".

**The failure it prevents is subtle.** A document that includes everything looks thorough and reads
as impenetrable, and the usual response is to skim it, which means missing the parts that mattered.
Splitting it doesn't lose information; it makes the information reachable. This is also why the
[change test](#placement-tests) and this rule pull in the same direction — depth kept in one dedicated
place is easier to keep current than depth scattered through prose that mostly isn't about it.

**Where it can go wrong:** a chain of thin documents, each linking onward without ever saying
anything, costs more than one honest page. The reader shouldn't have to follow three links to learn
one fact. Split when a section has grown its own audience, not to hit a length target.

## Structure documents as a journey

A document is read start to finish by someone who doesn't yet know the subject, and dipped into by
someone who does. Ordering the sections well serves both, and it's mostly a matter of putting things
in the order a reader can absorb them.

The shape that works, borrowed from how books are built:

1. **What this is and who it's for** — orientation, in a few lines. A reader who is in the wrong
   place should discover that immediately rather than three sections in.
2. **Background and context** — what someone needs to know before the main content makes sense.
   Keep it short and make it obviously skippable, with a heading that says what it is, so a reader
   who already has it can jump the section without wondering what they missed.
3. **The main content** — what the document is actually for, and the reason most people opened it.
   This is the part worth the most care, and it should start early enough that a reader scanning from
   the top reaches it quickly.
4. **Detail, edge cases, and reference** — exhaustive material that supports the main content but
   would drown it. Parameter tables, failure modes, migration notes, the full enumeration of options.
   Appendix material: present, findable, and out of the way.

The test is whether a reader can stop at any point and have gained something coherent. If
understanding section 2 requires section 5, the order is wrong.

**Order by what the reader needs, not by how the work happened.** Documents drift into narrating
their own construction — the investigation, then the options considered, then the decision. Readers
want the decision first and the reasoning available underneath. This is the same buried-lede problem
as in [human first drafts](plain-language.md#human-first-drafts), at document scale.

**Headings are the table of contents**, whether or not the document has one. A reader who scans only
the headings should come away with the document's shape and be able to find the section they need.
When that doesn't work, the headings are the problem — see
[headings are labels](plain-language.md#headings-are-labels-not-descriptions).

## One document or several

Every other placement test asks where a fact belongs. This one asks whether the **artifact** is one
thing. It's the same single-responsibility rule applied at the largest scale, and it's the easiest to
skip, because a document's size is the most visible thing about it and therefore the least likely to
feel like a finding.

**The test is different readers, not length.** A long reference page with one audience is fine. A
document is doing several jobs when its sections have different readers arriving with different
questions, and each has to scroll past the others. Signs:

- The top-level headings don't share an audience — a product thesis, a business stance and a coding
  style guide in one file.
- Whatever indexes or links to it describes only part of what's inside, so readers arrive expecting
  one thing and find another sitting alongside it.
- It's both the orientation page a newcomer is sent to *and* the deep reference someone returns to.
  Those want opposite treatments: short and linking, versus long and complete.
- Sections get cited individually from elsewhere, each by a different kind of document. That's
  evidence they're separate artifacts already, sharing a file by history.

**Cost it honestly rather than treating cost as a veto.** A split moves anchors, so inbound links
break. Say how many and from where, and what would keep them working — leaving a stub section that
links onward, or updating the references in the same change. "This should split, here is what breaks
and what it takes" is a usable suggestion. "This is too long" isn't, and "there are inbound links so
it can't move" is giving up early.

**If you decide against splitting, say so and why.** For a document that is visibly large, silence on
the question reads as approval, and the next reader has no idea whether it was considered.

## Learn the repo's conventions

You are editing someone else's repository. Before deciding that a fact is in the wrong place, find
out where this repo puts things — otherwise you'll propose restructuring toward a layout the project
deliberately doesn't use, which is worse than the problem you're fixing.

**Read the stated conventions first.** Whatever the project has written down about its own
documentation governs, and outranks anything in this skill:

- Contributor and style guidance, wherever it lives.
- Agent instruction files, at the repo root and in subdirectories — these often state exactly where
  docs belong, and a nested one may override the root for that subtree.
- Any documentation about the documentation: a docs index, a template, an ADR describing the layout.
- Instructions the caller gave you, which outrank all of the above.

**Then observe what the repo actually does.** Stated conventions go stale too, so check them against
practice:

- Where does prose live now? Alongside code, in a central tree, in a wiki or external site, in
  generated API reference, in commit history?
- What is documented in code comments versus in files, and how heavily?
- Is there an established entry point, and do documents link to each other or sit isolated?
- What are the naming and formatting habits — file names, heading style, diagram tooling?

**Where practice is consistent, follow it**, even if you'd have chosen differently. Consistency is
worth more than your preference, because a reader who has learned where things live can find the next
one. A suggestion that fits the repo's existing shape also has a far better chance of being accepted.

**Where practice is inconsistent, that's a finding** — but propose the convention the repo mostly
already follows rather than importing one. Say plainly that it's a convention question, since it
affects more than the file in front of you and the caller may want to decide it separately.

**Where there's no convention at all**, use judgement and say what you assumed. Some defaults that
travel well across most layouts: an entry point that orients a newcomer and links onward; overview
documentation kept near what it describes, so it's found and updated by whoever is working there;
contracts documented on the abstraction itself; and reasons for non-obvious code kept next to that
code. Offer these as reasoning, not as rules — a monorepo, a library with generated reference docs,
and a service with an external docs site all have good reasons to differ.

## Lifespan

Establish how long an artifact is meant to last before judging it, because the rules differ by class
and applying the wrong set does damage. Nagging a working note about duplication wastes everyone's
time; "correcting" a historical record destroys the thing it exists for.

| Class | Describes | Duplication | Links out to | Updated as reality changes |
|---|---|---|---|---|
| **Enduring** — reference docs, code, doc comments | how things are | one home, strictly | enduring things only | yes, must be |
| **In-flight** — plans, work in progress, design explorations | work happening or being considered | fine, expected | anything | yes, or deleted |
| **Frozen** — historical notes, decision records, incident writeups | how things were, at a moment | necessary | risky, targets rot | **never** |

**Enduring artifacts get the full ruleset.** Every placement test below, and the highest bar on
prose. These are read the most, live the longest, and cost the most when wrong.

**In-flight artifacts get a much lighter touch.** A plan restating a fact from three other documents
is *doing its job* — it's a working surface, and forcing the reader to follow links mid-task is worse
than the duplication. Links everywhere are fine. Status, open questions, and things known to be
changing all belong. They should still be tight and factual, since a confusing plan is expensive
while it's live, but don't apply the change test to them and don't propose restructuring something
scheduled for deletion. Be proportionate: a wip document usually deserves a few sentences of review,
not a report.

**Frozen artifacts must not be updated at all.** A note recording what was true in March is not stale
— it's accurate about March. Duplication in it is essential, because it has to stand alone once
everything it described has moved. The only valid findings are that it isn't clearly dated, isn't
clearly marked as a record, or has been edited to reflect later reality. If you catch yourself
proposing to bring a historical note "up to date", stop.

### The link-direction rule

**Enduring artifacts must not depend on in-flight ones.** The plan gets completed and deleted, or
abandoned, and the permanent document is left pointing at nothing — or at a proposal that never
happened, which is worse, because the reader believes it. In-flight documents linking to enduring
ones are fine and good.

The exception is a **status note**, clearly marked as temporary and not load-bearing: "this area is
being migrated, see [plan] for progress". That works because a reader who follows a dead link loses
nothing — the sentence around it still carries the fact.

The test: if the target disappeared tomorrow, does this document still make sense? If not, the fact
it needs should be stated here, in an enduring form.

### Temporary information wearing permanent clothes

The commonest and least visible version of the problem, because it looks like ordinary writing.

```csharp
// As per step 7
await index.CreateAsync();
```

Step 7 of what? The plan that said so is finished and deleted, and this comment now means nothing —
but it doesn't *look* like it means nothing. A future reader assumes it's meaningful, hunts for the
referent, finds nothing, and is left unsure whether they're missing something. A dead markdown link
at least announces itself. This just sits there.

The same defect in its other outfits:

- `// temporary workaround` — with no date and nothing saying what removes it. Three years later
  nobody dares touch it.
- `// TODO: remove after the migration` — which migration? It finished. Or didn't.
- `// don't change this until phase 2` — phases are a plan's vocabulary, not the codebase's.
- `// see the design doc` / `// per the ticket` — the reason lives somewhere with a different
  lifespan than the code.
- `// legacy` — relative to what, and as of when?
- Names carrying a moment in time: `NewOrderService`, `OrderServiceV2`, `ImprovedParser`,
  `LegacyClient`. "New" is a claim with an expiry date, and the next one is `NewNewOrderService`.

**The fix is to state the durable fact instead.** The reason a step existed usually *is* durable even
when the plan isn't:

> `// As per step 7` → `// The index must exist before the backfill runs, or the backfill table-scans.`

If the reason is genuinely temporary, keep it and make its temporariness checkable — date it and name
the condition that ends it: `// Workaround for upstream #4213, remove when we're on v3.2+`. That a
reader can act on.

**Watch for this at the boundary especially.** Text written *during* a piece of work absorbs that
work's vocabulary — steps, phases, "the new approach", "the old one" — and then stays in the codebase
after the work is a memory. When reviewing anything recently written alongside a plan, ask of each
reference: will this still mean something once the plan is gone?

### Telling the classes apart

Don't assume a directory layout. Work it out from what this repo does:

- **Where it sits**, judged against the repo's own conventions — a directory of plans, a wip or
  drafts area, an archive.
- **Markers**: frontmatter status, a date in the filename or heading, "draft", "proposal", "as of".
- **Language**: "we will", "proposed", "once this lands", "currently", open TODOs, unresolved
  questions.
- **What it's about**: work not yet done is in-flight; a system as it exists is enduring; a moment
  that has passed is frozen.

**When you can't tell, say so and ask** rather than guessing. Guessing picks a ruleset, and the wrong
one produces either wasted work or damage.

That difficulty is itself a finding. **A reader must be able to tell what they're holding**, and an
unmarked, undated proposal read as current documentation is how something nobody built becomes
something people believe exists. If an artifact's class isn't obvious, saying so is often the most
valuable thing in the report.

### Promotion

An in-flight document that now holds the only copy of a durable fact is a finding, and an easy one to
miss because nothing about it looks wrong. The work landed, the plan still carries the real
explanation of why, and the plan is on a deletion path.

Propose moving the durable part to an enduring home and letting the plan keep the working detail.
This is the one case where a wip document deserves close attention: not because it should meet the
enduring bar, but because something inside it should have been moved out.

## Placement tests

Apply these to any fact you find written down.

**Change.** If this fact changed tomorrow, how many places would need editing? One is correct. More
than one is a defect — pick the home and replace the others with links. This is the single most
useful question in this document.

**Ownership.** Which artifact would a reader naturally look in for this? That's its home, even if
it's currently written somewhere more convenient.

**Self-evidence.** Cover the prose. Can a competent reader get this from the code, the name, or the
signature? If yes, delete it.

**Level.** Does this sentence answer a question at a different zoom than the rest of the artifact? A
component overview that starts explaining a retry loop's backoff arithmetic has dropped a level; that
belongs next to the code.

**Staleness.** Will this text silently become wrong when the code changes, with nothing to catch it?
Text that enumerates things (implementations, parameters, file lists, step counts) goes stale
fastest. Prefer a link, or prose that describes the rule rather than the current membership.

## Leaky abstractions in prose

An abstraction exists so a caller can ignore what's behind it. Prose leaks when it drags the hidden
detail back into view.

The most common case is an interface or base type whose doc comment talks about its implementers:

> **Leaks:** "Implemented by `SqlOrderStore` and `InMemoryOrderStore`. The SQL version opens a
> transaction per call."
>
> **Doesn't leak:** "Persists and retrieves orders. Implementations must be safe to call from
> multiple threads, and must treat a missing order as `null` rather than throwing."

The second version tells a caller what they can rely on and an implementer what they must deliver.
It stays true when a third implementation appears; the first version goes stale that day.

Leaks run the other way too. A module README that explains why the whole system uses event sourcing
has reached up a rung — that belongs in the architecture doc, with the README linking to it.

## Discoverability

The goal is that someone landing on the repo cold can reach any document by following links, knowing
at each step which link to follow. The repo decides what the entry point is and where documents live;
these properties hold regardless:

- **There is an obvious entry point, and it orients rather than explains.** Whatever a newcomer hits
  first should say what this is and send them onward. When it has grown to hold the architecture as
  well, that's a placement finding.
- **Every document is linked from somewhere.** An unlinked document is invisible and will rot. When
  you find one, either link it from wherever its neighbours are listed or propose deleting it.
- **A directory with several documents has something that lists them**, with a line on what each is
  for, so a reader can choose without opening all of them.
- **Documents link to the code they describe**, ideally to the specific type. This is what keeps a
  doc honest — a link that stops resolving is a visible signal, unlike a paragraph that quietly
  became wrong.
- **Overview documentation is easier to find and keep current when it sits near what it describes.**
  Whoever is working in that area sees it, so it gets updated. Documentation about a component that
  lives far from the component tends to go stale unnoticed. This is a reason, not a rule — projects
  with a docs site, generated reference, or a monorepo layout have good grounds to centralise, and if
  this repo has already made that choice, work within it.

Prefer small documents that link to each other over one large document. A reader can skip a link;
they can't skip the middle of a page they're scanning.

## Reference by identity, not position

A cross-reference should name *what* it points at, not *where it currently sits*. Positional
references break silently: nothing errors, the reference simply starts pointing at the wrong thing,
which is worse than pointing at nothing because the reader has no signal to distrust it.

```csharp
// See note 7 in the architecture docs
```

Note 7 may be entirely correct today. But inserting a note earlier in that list — an ordinary,
low-risk edit that nobody would think to check for callers — makes this comment point at note 8's
content while still reading as authoritative. The target document is permanent and accurate; the
*reference* rotted.

The same defect in its other forms: "step 3", "section 4.2", "the third bullet", "as described
above", "see below", a line number like `SearchIndex.cs:42`, "the second parameter". All of them
encode an ordering that the next edit is free to change.

**Give the target a stable identifier and reference that.**

```csharp
// See #RATE-LIMIT in the architecture docs
// See IHQ-123 for why this ordering matters
```

An identifier survives reordering, rewording, and the document being split in two. It's also
**greppable in both directions**, which is the practical benefit: before editing a doc you can find
everything referring to a marker, and from a comment you can find the target. Neither is possible
with "note 7" — you cannot grep for a position.

What counts as stable, roughly best first:

- **An explicit named marker** in the target — `#RATE-LIMIT`, `[TENANT-ISOLATION]`. Costs a little
  machinery, survives everything, greps cleanly.
- **An external identifier** — a ticket, an ADR number, an RFC section. ADRs work well because they
  are append-only and never renumbered.
- **A heading anchor** — better than an ordinal, but drifts when the heading is reworded. Fine for
  ordinary links; weak for a reference that must not break.
- **A quoted phrase** from the target, when nothing else exists. Findable by search, and visibly
  wrong if the phrase disappears.

**The reference implies an obligation on the target.** If you propose `// See #RATE-LIMIT`, the
document needs a `#RATE-LIMIT` marker — say so in the same suggestion, or you have swapped a drifting
reference for a dangling one.

### Renaming things that are linked to

The rule is **check before you rename, not don't rename.** A heading with a bad name stays bad, and
"something links to it" is a cost to weigh rather than a reason to stop.

So: grep the repo for the anchor, the filename, the symbol. Then report what you found alongside the
suggestion, because that's what makes it decidable — "three inbound links, all in `docs/`, update
them in the same change" is a different proposal from "thirty inbound including the agent
instructions, so keep a stub". Where the project has a link checker, name it so the change can be
verified.

A rename with no check is the actual defect. It's silent, it breaks navigation for everyone
downstream, and nothing surfaces it until someone follows a link.

Be proportionate. Not every link needs a named anchor; a heading link between two documents that
change together is fine. Reach for a stable marker when the reference crosses a boundary that makes
breakage likely or expensive — code pointing into docs, one repo into another, or anything a reader
would follow while debugging.

## Scoping to the right repo

Information belongs in the repository that owns the thing it describes. Terraform conventions belong
in the infrastructure repo. Deployment runbooks belong wherever the deployment lives. An application
repo that carries a copy has just created a second source of truth that nobody will remember to
update.

When a document is in the wrong repo, say so. Where a cross-repo link is the right answer, propose
the link — a one-line pointer to the owning repo beats a copied section every time.

## Diagrams

Mermaid renders in most markdown viewers and lives in the file as text, so it diffs and reviews like
code. Reach for it when prose is describing:

- **Structure** — how components relate: `graph` / `flowchart`
- **A call or message flow** — who talks to whom, in order: `sequenceDiagram`
- **States and transitions**: `stateDiagram-v2`
- **Data shape and relationships**: `erDiagram`

The tell that a diagram is wanted: two or more paragraphs whose main content is nouns connected by
verbs ("the API publishes to the queue, which the worker consumes, which writes to the store").
That's a picture written out longhand, and it takes the reader far longer to assemble.

Keep diagrams at their artifact's altitude — an architecture diagram shows components, not method
calls. And keep them small; a diagram with thirty nodes has the same problem as a wall of text.

## Code as communication

Names and types are prose with a compiler attached. They're read more often than any comment, they
can't silently drift from the code, and a reader can't skip them. That makes them the highest-leverage
writing in the repo — and it means a lot of comment problems are really code problems.

**The move:** when prose exists to compensate for something the code could have said itself, propose
changing the code and deleting the prose. This is in scope for you. Flag it as a code change so the
caller knows what they're agreeing to, and offer the prose-only fallback where one exists.

### Naming

- A comment that only restates the name is redundant — but sometimes it's evidence the *name* is
  wrong. Ask which, and say so. `// returns true if the user can edit` above `CheckUser()` means the
  name should be `CanEdit()`.
- Names carry the same DRY concern as prose. `OrderService.ProcessOrder(Order order)` says "order"
  three times.
- Vague verbs — `Process`, `Handle`, `Manage`, `Do`, `Check` — are where a comment usually gets
  attached to explain what actually happens.
- Abbreviations and internal shorthand in a public name force every reader to learn vocabulary.
  Spell it out unless the abbreviation is genuinely more standard than the expansion (`Id`, `Url`,
  `Http`).
- A name that needs "and" in it is usually doing two jobs — that's the single responsibility
  principle showing up in the naming.

### Types

A type says the same thing as a comment, except it's checked and can't be ignored. Each of these is a
comment asking to be deleted:

| The comment says | The type should say |
|---|---|
| "must be one of `pending`, `settled`, `failed`" | an enum |
| "must be a well-formed account ID" | an `AccountId` type, not `string` |
| "in milliseconds" | a `TimeSpan` / `Duration`, not `int` |
| "may be null if the order hasn't shipped" | a nullable or option type, made explicit |
| "pass either `userId` or `email`, not both" | two overloads, or a union — make the illegal case unrepresentable |
| "don't mutate this after construction" | make it immutable |
| "call `Open()` before this" | a type that only exists once opened |

The last few are API shape rather than annotation, and are correspondingly bigger asks. Raise them
anyway — a doc comment explaining which argument combinations are valid is documentation standing in
for a design fix, and it will be re-read and re-misunderstood indefinitely.

Don't push this past the point where it's paying for itself. A wrapper type for every primitive is its
own kind of noise. The test is whether the constraint is one people actually get wrong.

## Listing values that change

Prose that lists *what a set of values currently is* goes stale faster than any other kind, and
nothing catches it. The code changes, the list doesn't, and now a reader has a confident, specific,
wrong answer — worse than no answer.

This shows up as:

- **A count of a list that immediately follows it** — "there are five stages:" above five bullets.
  The reader can count; the sentence can't be checked; and adding a sixth breaks it silently. The
  smallest and most common instance of this whole pattern.
- A doc listing an enum's members.
- A doc listing a config class's options, or a type's fields.
- A table of which value each environment sets.
- A README repeating a CLI's flags, or an API's response fields.
- A "supported X" list: providers, formats, regions, feature flags.

It compounds badly. A config class defines the available options; a deployment doc lists what each
environment sets them to; an architecture doc lists them a third time as background. One change now
needs three edits, and whichever copy the reader finds first is the one they'll believe.

**The fix is a link, plus the rule instead of the membership.** Link to the type, the config file, or
the generated reference — the definition is the source of truth, so send the reader there. Then, if
the doc needs to say something, say the thing that stays true: *why* the set exists, what governs
membership, what a reader should know when choosing. "Each environment sets `MaxConnections` to the
RDS instance's connection limit minus headroom for migrations" survives every change to the numbers.
The table of numbers doesn't.

Where the values genuinely must appear in prose — an example in a tutorial, a worked walkthrough —
make it obviously an illustration rather than a specification, and link to the real list.

### Configuration values have no single answer

Worth separating out, because it's the case where documenting a value isn't merely fragile but
impossible. A typical setting exists in layers: a default on the options class, a base config file,
then per-environment overrides. "The cache holds 10,000 entries" is then not stale-in-waiting — it's
already wrong in every environment that overrides it.

The trap is that prose stating the *default* looks correct on inspection. A reviewer comparing the
doc against the options class finds agreement and stops, while production runs a different number.
Checking a documented value means checking every layer that can override it, not just the one that
declares it.

Two things follow:

- **A per-environment table is not the fix.** It duplicates machine-readable data from several files,
  goes stale at the next deploy, and gives no answer for an environment it doesn't list. It also
  tends to omit the interesting override — the one where a setting is disabled entirely.
- **Document the mechanism and name the keys.** What the setting does, what changes when it moves,
  what constrains a sensible value, and what the key is called — then link to the config. That stays
  true across every environment and every change, and it's what someone tuning the value actually
  needs. A reader who wants today's number is one link from it and will get the right one.

**Generate it, or link it.** If a list truly needs to be in the docs and kept current, it should be
generated from the source rather than typed.

## Commit messages and PR descriptions

These are the one form of prose that can't be edited once it's out, and they're read in a list, so
economy matters more than anywhere else.

- The subject line states what changed, in the imperative, at the altitude of the change: "Cap RDS
  connections by moving the worker to ECS", not "Various fixes".
- The body carries what the diff can't: why, what was rejected, what a reviewer should watch for.
  Never a summary of the files changed — the diff is right there.
- **Ask whether the explanation belongs in the repo instead.** A long commit body explaining how a
  subsystem works is documentation that will only ever be found by someone running `git log` on the
  right file. If it's durable knowledge, propose moving it to a doc or a comment and leaving a short
  message behind.
- PR descriptions answer "what should I look at, and what do I need to know to review it". Not a
  restatement of the commits.
