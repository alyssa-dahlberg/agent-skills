# Design notes

For anyone editing this skill. Not loaded when the skill runs, and deliberately so. An agent using
the skill needs to know what to do, not why it ended up this shape.

Records the decisions that aren't obvious from `SKILL.md`, the evidence behind them, and what was
tried and rejected. When you change something here, change the note with it. A design rationale that
no longer matches the skill is worse than none.

## Why the skill exists

Two failures in codebase prose, which turned out to be one failure:

1. **Information sprawls.** The same fact lands in a module doc, an architecture doc, and a class
   comment. They drift, and the reader who finds the stale copy is worse off than if nothing had been
   written. Models cause this readily: asked to document something, they cover it everywhere and
   count that as thorough.
2. **Prose fills space it doesn't have facts for.** Flourishes, hedges, balanced clauses, and
   rhetorical shapes accumulate where a concrete statement belongs.

Both are the same defect at different scales: text that isn't committing to a fact. That's why
placement and prose are one skill rather than two, and why placement runs first, since accepting a
placement fix often deletes the prose a rewrite was about to polish.

## Decisions and the reasoning

### Two passes, author then fresh subagent

The most load-bearing decision, and the one most likely to be "simplified" away by someone who reads
pass 1 as redundant. It isn't.

**Evidence.** One model wrote an architecture doc from a seven-fact brief, then reviewed it twice:
once in the authoring context, once by a fresh agent given the identical review prompt.

- Self-review found 25 issues and cut ~180–200 words, mostly by **deleting whole sentences**,
  including a closing section that recapped the body.
- The fresh reviewer opened with "the draft is already tightly written", found ~18, and cut ~40 words,
  almost all **word substitutions** (`for the duration of` → `during`).
- They directly conflicted three times. The fresh reviewer **defended** a tricolon and a doubled
  phrase as "intentional rhetorical repetition"; the author knew both were accidents.
- Self-review caught three of its own **fabrications**: an invented retention period, an invented
  legal rationale, an unchecked "independent". The fresh reviewer could not have: given only the
  document, an invention reads exactly like a fact the author knows.

**Conclusion.** Fresh context is not strictly better, which is what an earlier draft of this skill
claimed. It is better for reader-experience defects (does this parse, is this ambiguous, is this
already said elsewhere) and structurally blind to provenance and intent. A fresh editor's systematic
bias is *deference*: unable to tell craft from artifact, it protects both.

**If you revise this:** don't reorder the passes and don't merge them. Pass 1's answers do not
survive into the next context.

### The catalogue is a spec, not instructions

**Evidence from the anchoring experiment.** A fixture seeded with six catalogued prose tells and six
defects only findable by checking the doc against the code (a wrong TTL, sliding-vs-absolute, a stale
region count, "a few times" where the code says 2, a dead link, and "oldest entry" contradicting LRU).
Three conditions, same input:

| | non-catalogued (6) | catalogued tells | root-cause synthesis |
|---|---|---|---|
| full skill | 6/6 | all | yes |
| catalogue stripped (`plain-language.md` 338→164 lines) | 6/6 | all | yes |
| no skill | 6/6 | all | no |

Two hypotheses died here. The catalogue is **not** harmful: the full-skill run scored 6/6 and stated
it had verified every claim against the code, so the earlier misses came from the version predating
the verify-claims instruction. And it is **not** additive: the stripped run matched it on every
dimension, including all the prose tells, and asked a better question about which source was
authoritative.

What the skill contributed over baseline in all conditions was the *synthesis*: baseline listed four
contradictions, the skill named one cause with four symptoms and gave a rule preventing the next.
That comes from the placement framework, not the pattern lists.

**The idea that produced pass 3, which is worth keeping even though the pass is gone.** A checklist
consulted *after* an independent reading is a safety net; the same checklist consulted *during* it
becomes the frame and narrows what gets noticed. Same content, different timing, different outcome.
That is the same shape as the pass 1 / pass 2 finding, where *when* a reviewer sees something changes
what they find, and it is why `plain-language.md` teaches how to weigh patterns without listing them.

An intermediate version tried to enforce this by instruction: keep the enumerations in
`plain-language.md` and tell pass 2 not to read them. An outside review pointed out that leaked twice
over, since the file was handed to pass 2 anyway and `SKILL.md` named the patterns itself. The fix at
the time was to move them to a separate file; the fix now is that the general catalogue isn't in the
runtime path at all.

**A few named patterns came back later, and that is not a reversal.** `plain-language.md` names em
dashes, misleading first reads, paragraphs that are really lists, and offhand phrasing kept as voice.
Each was added for a reason recorded below, and the reasons share a shape: these are the cases where
an editor working from judgement alone walks past the defect, or talks itself out of the fix. A
catalogue narrows an independent reading; a handful of named exceptions to that reading doesn't. If
this list grows much beyond a handful, that argument has stopped being true and the catalogue is
coming back by instalments.

**An argument that does not work:** an earlier note here claimed pass 3's yield would measure the
catalogue's value over time. It can't. Runs are stateless and nobody aggregates outcomes across them,
so the question never gets answered by itself. Deciding it needs a deliberate check.

**The deliberate check, run once.** Pass 2 (Opus, catalogue withheld) reviewed the argued-prose
fixture, then pass 3 (Haiku, catalogue only) swept it with pass 2's findings in hand. Pass 3 returned
nothing new, having examined four candidates and given a sound reason for rejecting each, so the
pass works and there was simply nothing there.

That is the third independent result pointing the same way, after the anchoring experiment and the
no-skill baseline. It also weakens the last defence being held open for the catalogue, that a weaker
model would need the list: Haiku *with* it found nothing Opus *without* it had missed.

**Resolution: the list became a spec rather than being deleted.** It now lives at
[evals/detection-spec.md](evals/detection-spec.md), which records what the skill is expected to catch, with a
coverage table mapping each pattern to the fixture that exercises it. Nothing loads it at runtime,
and pass 3 was removed with it, since a sweep needs something to sweep with.

Deleting would have thrown away the useful part. The list is a decent statement of what good output
looks like, and it dates the claim: *as of August 2026, on Opus 5 and Haiku 4.5, these are recognised
unaided.* If a future model stops catching something on it, this is what to put back, and the
coverage table says which fixture would show it.

The coverage table is also honestly unflattering, since a third of the entries have no fixture, so
"models handle these unaided" currently rests on the ones that happen to be seeded. The word-level
gaps are cheap to close by adding to an existing fixture. Uniform cadence is genuinely hard to seed,
because it only exists at document scale.

Removing pass 3 also collapsed the flow back to two passes, which an outside review had called the
most fragile part of the design.

**Caveats on the experiment:** one document, one run per condition, and the seeded tells were obvious
(`utilise`, "the one thing you must know"). It rules out a large effect, not a small one, and says
nothing about weaker models, subtler prose, or run-to-run variance. The framing sections of
`plain-language.md` (density weighting, what not to cut, human drafts) were kept in *both* skill
conditions and are untested.

### Editing, not completeness, and standalone

Both cold runs showed the same split: the no-skill baseline was better at finding what *isn't*
written (missing prerequisites, no verification step, no teardown), while the skill was better at
what *is* written. That split is intended, not a shortfall.

The reasoning: reviewing text and auditing coverage are different jobs with different inputs. Judging
that a setup guide needs a teardown section requires knowing what setup guides ought to contain,
which is scope knowledge rather than editing. It also has no natural stopping point, and a list of things that could
be documented buries the edits that were actually asked for.

The distinction that makes this workable is internal versus external. A document failing on its own
terms (an intro promising two reasons and giving one, a section omitting a command four others
assume) is in scope, because careful reading reveals it. "There should also be a section on X" is
not.

**Standalone by design.** The skill assumes nothing about what else a project runs, and reports
shouldn't suggest that some other process will catch what this one skipped. Whether coverage is
handled by a PR review, a docs lens, a person, or nobody is the reader's business. What the skill
owes them is an accurate statement of what it did and didn't check, which `report-format.md` now
requires.

### Suggestions, not edits

Editing prose is judgement and voice, and the author owns both. Also practical: a report the caller
walks through produces better outcomes than silent rewriting, because rejections are visible.

Reports must carry paste-ready replacement text. "Consider tightening this" hands the work back and
was an explicit failure mode in early drafts.

### Iterate until clean

Applying suggestions is itself writing, so it introduces new tics and strands references. Findings
also mask each other: a reviewer proposing to delete a duplicated section never examines the prose
inside it.

**This is reasoning, not evidence.** The loop has never been run end to end, and `SKILL.md` says so
in place rather than asserting a round count.

Rejections must be carried forward, or each round re-raises settled points and reports grow instead
of shrinking.

### Judgement over rules

Every pattern in `evals/detection-spec.md` is correct somewhere. The skill says so repeatedly and
on purpose: a version that reads as a checklist produces rule-citing noise, and authors learn to skip
the reports. Hence "density is the signal", the instruction to count before claiming a habit, and the
refusal to ship a banned-word list.

This is also why the skill asks for a strong model, and the most *different* one available. A model
is worst at spotting the tics it produces itself, so a review from the same lineage as the writing
can return a clean bill that only means both write the same way.

### Cross-family consultation: tried, then removed (August 2026)

`SKILL.md` carried an optional step telling a run to ask a model from another family about the prose,
on the argument that recognising its own tics is the one thing a same-lineage reviewer can't do. The
argument still looks right. The step didn't pay for its space.

It needed correcting twice before it was dropped. An intermediate version had the *editing pass*
dispatched to a different family, which doesn't work in general: pass 2 earns its place by exploring
the repo, so whatever runs it must be able to. The next version described one local setup's
constraints (no file access, one question per call, paste the text rather than a path) as though they
were properties of the idea, when someone else's access to another family might be a full agent that
reads files perfectly well.

What settled it was using it. Run against `SKILL.md` itself, a local Gemma 26B returned seven
findings: two correct but trivial cuts, two that agreed with what the main pass had already found,
one that made an aphorism longer, and two proposed rewrites of the antithetical frame that
reintroduced the frame they had just flagged. One opinion, for a section of the skill and a minute
per call.

The general lesson outlives the step: **when writing about capability that varies by environment, say
what the caller should establish, not what you happen to know about one setup.**

### Two patterns where the fix adds words

Almost everything in this skill cuts. Two additions run the other way, and they are grouped here
because that shared property is what makes them easy for an editor to miss or to argue out of.

**Sentences that mislead on first read.** Linguistics calls the extreme case a garden-path sentence;
Joseph Williams calls the everyday case a miscue. The skill's author raised it from a real example:
"from the single decode base generation already holds", where the reader takes "the single decode
base generation" as a noun phrase and then finds a verb with nothing to attach to. Two documented
causes stack there, so the guidance names both rather than treating it as one defect:

- **The dropped relativizer**, which the plain-English literature ties directly to over-application
  of "omit needless words". Restoring "that" is a one-word fix.
- **Noun stacks**, where the plain-language guidance is unusually concrete: readers "think they've
  found the noun when they're still reading adjectives"; two nouns are fine, three wants checking,
  four is unreadable; fix by hyphenating, unpacking with prepositions, or abbreviating. The scientific
  writing sources add the sharper point that a stack is often *irrecoverably* ambiguous rather than
  merely slow, since the missing relationship isn't in the sentence to be recovered.

This is pass 2 material by construction. The author knows which reading was intended, so the wrong
parse never occurs to them, which makes it one of the clearest cases where a fresh reader sees
something the writer structurally cannot.

**Paragraphs that are really lists.** Also raised from a real example, where six parallel facts about
a worker's shape were packed into two sentences. The point that made it worth a section: **nothing
needs cutting and no wording needs improving.** The defect is entirely presentational, which is
exactly why a reviewer tuned to word-level tells reads the paragraph, finds no bad words, and moves
on. The skill already had "turn a clause pile into bullets" as one line in the rewrite moves; that
was too small for how often it applies.

The guard against overuse is stated with it: bulleting an inventory rescues it, bulleting an argument
destroys it, because the connective tissue between the claims is a fact too.

**Why both need explicit permission to add words.** An editor that has absorbed the rest of this
skill will resist a suggestion that lengthens a sentence, and an author will read it as padding. So
both entries say plainly that the repair adds a word and that this is the correct trade. Ambiguity
costs more than three syllables.

### Em dashes are the one exception to the density rule

Everywhere else this skill refuses to flag a pattern on sight, and that refusal is load-bearing:
rule-citing reports get ignored. The em dash gets a harsher default anyway: look at every one.

Three reasons, and the third is the one that decided it.

**It is a decision not made.** The mark joins two clauses without stating the relation. That's why
it's easy to write and why it so often marks a sentence the author hadn't finished thinking through.
The fix is naming the relation, which is a real edit rather than a substitution.

**It is contagious.** This came from the skill's author, who reports almost never using em dashes and
having started producing them from exposure to model output. That makes the mark unlike a style word:
its rate in a repo climbs without anyone choosing it, so "the neighbours write this way" is evidence
of drift rather than of house style. Same mechanism as
[voice: protect intent, not provenance](#voice-protect-intent-not-provenance): a habit that arrived
from outside gets defended as the author's.

**The corpus baseline was being used backwards.** `measure.py` prints a published-prose range, and a
review cited "within the human range" to leave two dashes in a three-paragraph document that was
badly overloaded. The range is drawn largely from writing where the em dash is a deliberate
instrument, so it says nothing about a specific technical sentence. The tool's comment and the
fixture key now both say the numbers test a habit claim across a document and never acquit an
individual mark.

**What stops this becoming a sweep.** Two guards. Recasting must change how the sentence is built, since
swapping in a comma leaves the overload and hides the evidence. And the report gives one finding with
a count plus two or three worked fixes, not one entry per dash, because twenty punctuation entries
bury everything that matters more.

### Voice: protect intent, not provenance

"Don't flatten voice into a monotone" was over-applying. Observed case: an author dictated "then we
can scale up resource to crush it", and the phrase came back as a `## Scale to crush` heading and was
then defended on later passes as the author's voice. The author had not chosen a vocabulary; they had
said a thing.

The fix isn't to drop the voice protection, which stops the skill producing clipped robotic prose. It
is to state what the protection covers. Two lines split cleanly:

- **Intent**: a metaphor doing explanatory work, a coined name used consistently, sentence rhythm.
  Keep.
- **Provenance**: a phrase that exists only because someone said it once, usually in speech or a
  chat message, promoted into a heading or a motif. Cut.

Pass 2 cannot tell these apart from the page, which is the deference weakness in its most durable
form: the phrase looks like style, so each editor preserves it, and preservation makes it look more
like style to the next one. So the guidance is a test the editor can run without knowing intent
(does it carry a fact a plain word wouldn't, would a stranger follow it, would the author write it
cold), and an instruction to name which test failed, so the author can answer "it was deliberate".

Headings and identifiers get called out separately because the cost concentrates there: a heading is
an index entry, a link target, and a search term at once, and it sets the register for everything
under it.

### Scope: decline the rules, not the request

The skill is for factual technical writing. Applied to fiction, poetry, or marketing it strips what
makes them work.

**Evidence.** Given a fiction fragment and a loaded request to "tighten it", an early version
declined and offered to help if asked again. The no-skill baseline protected the load-bearing
material *and* delivered the edit. The skill made the agent worse.

Current wording: say the rules don't apply and why, then help with ordinary editorial judgement in the
same turn.

The reason the rules don't apply is worth keeping: a closed text has no maintenance cost, so the
duplication argument driving Job 1 has nothing to bite on, and repetition is often refrain.

### Progressive disclosure inside the skill

`SKILL.md` states each principle in a sentence or two and links out. The reference file owns the
examples, tables, caveats, and limits.

**Evidence.** An earlier `SKILL.md` reproduced roughly a third of `reference/`, including caveats. A
review found nine near-verbatim pairs and made the argument that settled it: an agent that has read
`SKILL.md` no longer has a reason to open the reference files, so duplicating upward defeats the
structure it's part of. Duplicated *caveats* are pure cost: a caveat only matters to someone already
in the detail.

**If you add to `SKILL.md`:** ask whether it's a principle or an elaboration. Elaborations go down.

### No repo layout assumptions

The skill describes levels of detail as a scale, not as a table of files, and tells the editor to
learn the repo's conventions before judging placement. An earlier version hardcoded
`README.md` → `docs/` → module README → doc comment, which is one convention among many and would
have produced confident, wrong restructuring suggestions in any repo shaped differently.

Ordering: caller's instructions, then the project's stated conventions, then observed practice, then
this skill's defaults last.

### Terminology

"Altitude" is declared shorthand, introduced once, with a note not to use it in reports unexplained.
An earlier version used "the altitude ladder" as though it were established vocabulary.

Same correction applied to "the enumeration trap" (now "listing values that change"). Naming a
phenomenon is useful shorthand once a reader knows it and pure friction before.

## How much to trust the evidence below

Two tiers, and they should not be cited interchangeably.

**Clean.** The self-review asymmetry result. A subagent wrote a document from a fact list with no
skill loaded, then self-reviewed with no skill and no patterns named, and caught its own fabrications
and its own padding. Nothing in that loop had seen the catalogue, so pass 1's value doesn't depend on
anyone having been told what to look for.

**Circular.** Everything based on the synthetic fixtures. They were built by seeding defects from a
list already written, so finding them demonstrates that planted things can be found. Useful as
regression tests, not as proof of capability, and the scoring has the same problem: a report was
judged good when it matched expectations that came from the same source.

**Cold tests are the evidence that counts.** Two so far, both against real documents in another repo
that nobody here wrote or read first, both paired with a no-skill baseline.

*Run 1, on AI-written product and services docs.* The skill found five cross-file duplications the
baseline missed, and gave the opposite prescription on two documents disagreeing about account
ownership: baseline said "sync them", the skill said "delete one list", having spotted that both
files carried a note asking a human to keep them in step.

*Run 2, on a developer setup guide and an ops runbook, genres no fixture covers.* Both runs found the
top defect (a command referenced four times and never documented). Only the skill found: a paragraph
claiming a single source of truth while quoting the values a second time; an enduring runbook linking
to a todo item that will be deleted when done; an intro promising "two confidently-wrong diagnoses"
where only one is ever named; and "psychologically available" as a borrowed term of art in an ops
document. All verified against the files afterwards. It also classified the runbook as enduring while
treating the incident details inside it as frozen, and correctly reported that it could not run pass 1
by asking the author which specific claims had been checked rather than guessing.

**What the baseline does better, in both runs:** finding what *isn't* written. Missing prerequisites,
no verification step, no teardown, unexplained jargon. The skill scopes that out as documentation
auditing rather than editing, which is a defensible line but means the two are complementary. If
someone wants a gap analysis, this is the wrong tool and should say so.

Anyone extending this should add cold tests before adding fixtures. The fixtures are already the
well-covered part.

## Evidence log

Four with-skill / without-skill pairs, plus the asymmetry and anchoring experiments above. The
fixtures and their answer keys are in [evals/](evals/README.md).

| Eval | Result |
|---|---|
| Real AI-written docs (~1000 lines) | **Skill won clearly.** Found five cross-file duplications baseline missed. On two docs that disagreed about account ownership, baseline said "sync them", the skill said "delete one list", so baseline institutionalised the duplication. Skill also grepped for inbound anchors before proposing heading renames, and withheld a valid finding as a repo-wide convention question. Cost ~2× baseline. |
| Commit message | **Skill won on proportionality.** 4 bullets vs baseline's 7-section report for ten lines. Skill's rewrite deleted the backoff schedule and linked to the code; baseline reproduced it. But the skill **missed a factual contradiction** baseline caught. |
| Planted duplicate (3 files) | **Split.** Skill more disciplined, better choice of home, no scope creep. Baseline found more substantive gaps, including an undefined "20% jitter". |
| Fiction fragment | **Skill lost.** See scope decision above. |

Fixes that came directly from these: the ambiguity test, verifying checkable claims, counting before
claiming density, the out-of-scope rewrite, and preferring deletions to substitutions.

## Known weaknesses

- **The pattern enumerations are close to inert.** Tested directly (see the anchoring experiment).
  Cutting them changed nothing measurable. They now live in `evals/detection-spec.md`, outside the
  skill's own instructions, so nothing loads them at runtime at all. An earlier version of this note
  made the cross-family consultation their last justification and said to delete them once that
  stopped being how anyone used the file. That condition fired in August 2026, and the answer on
  review was to keep them: the coverage table maps each pattern to the fixture exercising it, and
  "what to put back if a future model stops catching this" is the list itself. The delete-rule was
  written as though the consultation were the only remaining use, which the same file contradicts
  three lines earlier. An outside review pointed out that the
  "pass 3 measures its own worth" argument cannot work, because runs are stateless and nobody
  aggregates outcomes across them.
- **Waffle correlates with the writing task more than the model, but the effect is smaller than it
  first looked.** Given a tight fact brief, the model produced 849 words with zero style words, zero
  hedges, and no inflated verbs. Given a vague philosophical brief and a word target, it produced 936
  words at 11.8 em dashes per 1000 (vs 9.4), 3 emphasis crutches (vs 0), and 2 inflated verbs (vs 0),
  a real difference, not a dramatic one, because the writer anchored the piece on a worked example
  rather than padding. Both fixtures are in `evals/`. The tells that did appear were rhetorical
  (antithesis frames, dramatic emphasis) rather than lexical, which supports weighting rhythm over
  vocabulary. The skill still treats this at sentence level and never asks the structural question
  directly: is this document filling space it has no facts for?
- **Cost.** Roughly 2× baseline tokens on a large document, before iteration. Justified for prose read
  many times by people and models; not for a throwaway note.
- **The iteration loop is untested.** Round two has never been run end to end. `SKILL.md` now says so
  in place rather than asserting a round count it has no evidence for.

## Rejected alternatives

- **A scoring rubric** (as in several published de-slop skills). Invites optimising a number instead
  of fixing the sentence.
- **Banned-word lists as rules.** Easy to check, easy to evade, dates quickly, and produces noise.
  Rhythm gives writing away more reliably than vocabulary.
- **Editing in place by default.** Removes the author's judgement from decisions that are theirs.
- **Depending on a companion review skill.** This one stands alone; a project's own standards outrank
  it where they exist.
- **Hand-maintained contents blocks** in the reference files. Deleted after one drifted within a
  single edit cycle. The skill's own rule is "generate it, or link it".

## Trigger accuracy

Measured in August 2026, after two false starts that are worth more than the numbers.

**The old harness could not detect a trigger at all.** `skill-creator`'s `run_eval.py` returned 0 on
every query, positives and negatives alike, across three iterations and every candidate description,
and those zeros were read as a weak description for a while. They were the instrument. It registers
the skill under test by writing into `.claude/commands/`, which produces a *slash command*. Reading
the session init event shows why that can never work: a file in `.claude/commands/` appears in
`slash_commands` and never in `skills`, and slash commands are invoked by the user rather than chosen
by the model, so the `Skill` tool call the harness watches for cannot happen. A second bug would have
survived the first: it returns false at the first tool call that isn't `Skill` or `Read`, so a run
opening with `Glob` or `TodoWrite` scores as a miss even when it calls the skill immediately after.

`evals/trigger_eval.py` replaces it, in this repo rather than as a patch, because the plugin file
lives in a marketplace cache and a patch would be reverted on the next update. It installs a real
skill into a throwaway project and scans the whole run. It leads with a self-test for exactly the
reason above.

**The second false start was the fixture.** The first real run scored 0/10 on positives. The queries
name files (`apps/payments/README.md`), the throwaway project seeded them as one-line placeholders,
and every positive run spent its turn with `Read` and `Bash` discovering there was nothing to edit.
Seeding a few hundred words of mediocre prose instead took the same description from 0/10 to 7/10.
**A trigger fixture has to contain work worth doing**, or it measures whether the model can find the
file.

Three descriptions, 20 queries, 3 runs each, same seeded project and model:

| | | positive fires | queries passing | false fires |
|---|---|---|---|---|
| **A** | the shipped description, 155 words | 19/30 | 7/10 | 0/30 |
| **B** | rewritten to 105 words, tells list cut | 15/30 | 5/10 | 1/30 |
| **C** | keywords restored, capability clause added, 145 words | 17/30 | 6/10 | 2/30 |

**A is what ships.** Nothing beat it, and it is the only arm with no false fires. B came out of an
editorial pass that cut the description's list of tells as context pollution, on the argument that
the skill spends `plain-language.md` keeping exactly that catalogue out of the runtime path. The
argument misapplies a Job 2 rule to a field that is not prose: a description is matching surface,
read to decide whether to open the skill, and once it fires the body governs. A description
restating the body is duplication worth paying for.

**Don't over-read the per-query differences.** The obvious causal story, that each regression traces
to a phrase B cut, survives one test out of three: restoring "restating it in three documents that
drift apart" moved the duplication query back (3→1→2), but restoring "marketing headings" did not
recover the headings query (2→0→0) and restoring "dictation tics" did not recover the dictation
query (3→2→2). At three runs a query, a 2/3 result is not a signal. The arm totals order
consistently on both measures; the individual queries mostly don't.

### Inviting use harder does nothing

A second round at five runs a query tested whether a more insistent invitation raises the rate. D
anchored it to a moment in the workflow ("run it over any writing you are about to hand over, before
opening a PR or asking for review"). E went as far as the field allows ("use on everything").

| | recall | wasted fires | scope-adjacent fires |
|---|---|---|---|
| **A** incumbent | 32/50 | 1/35 | 0/15 |
| **D** before a PR | 31/50 | 1/35 | 0/15 |
| **E** use on everything | 31/50 | 2/35 | 0/15 |

**The invitation clause is inert.** It moved nothing in either direction, and the precision cost that
was the reason for caution never appeared: the three negatives where firing would be defensible
anyway (fiction, landing-page copy, a launch blog post, all cases where the skill's documented
response is to say the rules don't apply and then help) drew zero fires in every arm. Note also that
the description has only about 58 characters of headroom under the 1024 limit, so any addition is
paid for by a deletion. D and E both bought their clause by cutting "reviews what is written rather
than auditing for what is missing", which cost nothing measurable.

**What decides it is the shape of the request, not the wording of the description.** Three positives
failed 0/15 in every arm: the 12-line commit message, doc comments on `IOrderStore` naming a
concrete implementation, and a setup guide contradicting `appsettings`. The tempting read is that
these are the non-markdown cases and the description leads with markdown. That does not survive
contact with the text: the description already names code comments, doc comments and commit messages
in its second sentence, and naming them plainly is not enough.

The queries that fire are open-ended and large ("does it read alright?", "what should move out or get
cut", "check the writing quality", and a duplication spanning three files). The queries that never
fire all hand the model a diagnosed defect in a single small artifact, and it simply does the fix.
This is the risk this section always named, now with evidence: a model consults a skill mainly for
work it cannot already do. It is unlikely to be fixable from the description at all, so the lever, if
one is wanted, is outside it: a project instruction, or a hook.

## Re-running the evaluation

`skill-creator`'s `quick_validate.py` catches frontmatter breakage, and it has already caught an
unquoted colon in the description (which would have stopped the skill loading) and a description over
the 1024-character limit. Run it after any frontmatter edit. The colon mistake recurred in August
2026, in a rewrite that began "Out of scope: fiction", so treat it as a standing hazard rather than a
one-off: the description is a single-line YAML scalar and any natural-sounding `word: word` breaks it.

For trigger accuracy, `evals/trigger_eval.py`, self-test first. For behavioural evals, see
[evals/README.md](evals/README.md) for the fixtures, their answer keys, and
the two methodology traps that caught us during development: baselines are strong, so always run one;
and a review-shaped prompt flatters the baseline by putting it in critic mode, which is not how the
skill is actually used.
