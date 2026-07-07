# review-lenses

A composable review system for coding agents. One orchestrator, many **lenses** — small markdown files,
each describing a single concern to review through. You extend it by dropping in a file, not by editing
the tool. It's built to be **project-specific and extensible at once**: the machinery is generic, all
the tailoring lives in lenses you write.

**The base skill is deliberately opinion-free — a neutral engine. The opinions are yours, and they live
in the lenses.** That's the whole point: this was built so its author could run a *highly tailored*
review process over their own repos — their conventions, their footguns, their taste — and the engine
was shipped so anyone can layer *their own* opinionated review on top. Same machinery in every install;
a completely different review depending on whose lenses are in `.review-lenses/`.

The lens set is meant to grow with your project — this is a *many lenses* system, not a handful.
For scale: the author runs about **18 lenses** at the time of writing. The examples here are a
starting palette, not the intended total.

## The idea

Two independent axes:

- **Lens** — *what to look for*: a concern (testing, a language's conventions, a compliance standard,
  comment quality, architecture, …). One markdown file per lens, in `.review-lenses/`.
- **Target** — *what to look at*: a diff, a class, a plan phase, a whole plan, a design doc, an idea.

A **job** is one lens on one target. You ask in plain English — *"review this branch"*, *"check the
payment flow against PCI concerns"*, *"review the architecture of these interfaces"*, *"sanity-check
this idea"* — and the orchestrator resolves that into jobs, dispatches a read-only reviewer for each,
loops on any lead worth chasing, and collates **one report**.

The key move: **a lens is data, read fresh every run.** If a lens cites references — local docs or a
URL — the reviewer opens them at review time, so findings track the source and never drift from a
paraphrase baked into a prompt. Conventions live where they belong; the review layer is where "does
this follow them?" actually gets answered.

## A strong `docs/` folder pays double

The author keeps a rich, human-readable `docs/` folder in every repo — architecture, conventions, the
*why* behind decisions — written for people first. Review lenses then **cite those docs instead of
restating them**, so the same words that onboard a human also drive the review, and neither can drift
from the other without the other noticing. The two go hand in hand: when you're deciding where a
convention should live, write it in `docs/` for the humans and point a lens at it. A reference-backed
lens over a good docs folder is the ideal end state; self-contained lenses are how you start before the
docs exist.

## Composable, isolated, and cheap to experiment

Every lens runs as its own **read-only subagent, in parallel, in isolation.** The orchestrator
dispatches them and only the *collated findings* come back — all the file-reading and reasoning each
reviewer does stays in its own context, never in yours. Two things follow:

- **Adding lenses is nearly free** for your context window and your attention. Ten lenses aren't ten
  times the context in the main loop; they're ten small isolated reviews and one merged report. A big
  lens set doesn't bloat anything or blow up a single giant context.
- **You can afford to be niche.** Because a lens is cheap, self-contained, and can't poison the main
  context, it's worth writing one for something *very* specific — British-English spelling in
  user-facing strings, a naming quirk you keep tripping over, one library footgun, a house rule nobody
  remembers. Write it, drop it in `.review-lenses/`, and experiment; if it's noisy, tune it or delete
  it. The system is meant to be extended by accretion — reach for a new lens freely.

## Self-serve review

Review isn't only a thing a human asks for. Any agent can invoke this skill on its **own** work —
before finalizing a change, after touching anything sensitive, when it's unsure — and get back
structured findings it can act on without a human in the loop. That's the intended habit: conventions
get applied *before* your attention is spent, not after. The skill's description tells agents this, so
a capable harness reaches for it on its own; nothing stops you asking explicitly too.

## Setup

1. Install the skill (see the repo root README for `npx skills` usage).
2. Create a **`.review-lenses/`** directory at your repo root — this is where *your* lenses live. It's
   deliberately not tied to any one agent's config directory: lenses are project data you author and
   grow, not agent plumbing. To keep them somewhere else, set the `REVIEW_LENSES_DIR` environment
   variable; how you set it depends on your harness (e.g. in Claude Code, add it to
   `.claude/settings.json`):
   ```json
   { "env": { "REVIEW_LENSES_DIR": "config/review-lenses" } }
   ```
3. Seed it from the [`examples/`](examples/) shipped here — copy the ones that fit, edit them, delete
   the rest. Then add your own.

That's it. Ask an agent to "review this branch" and it discovers your lenses automatically.

## The example lenses

The [`examples/`](examples/) directory is a starting palette — copy and adapt, don't use verbatim.
They're chosen to show the **different shapes** a lens takes:

| Example | Shape | Shows |
|---|---|---|
| [`csharp-conventions.md`](examples/csharp-conventions.md) | reference-backed (URLs) | Holding code to a published style guide; swap in your team's own standard doc. |
| [`pci-dss.md`](examples/pci-dss.md) | reference-backed (external standard) | Reviewing against a compliance/regulatory standard the reviewer fetches live. |
| [`testing.md`](examples/testing.md) | self-contained | A universal concern with no single canonical doc — the checklist lives in the lens. |
| [`docs-and-comments.md`](examples/docs-and-comments.md) | self-contained, broad triggers | A cross-cutting concern (comment quality, altitude) that applies to almost any diff. |
| [`banned-patterns.md`](examples/banned-patterns.md) | prescriptive / scripted | Handing the reviewer exact `rg` commands for known-bad patterns — mostly deterministic findings, with a quick sanity-filter on the fuzzy checks (the secret heuristic). |
| [`removed-behavior.md`](examples/removed-behavior.md) | self-contained, diff-shaped | Reviewing the *deletions* — a guard, error path, validation, or test dropped without being re-established. |

Each also shows the higher-quality moves: an opening **`Context`** paragraph (who the team is, what
they value) so the reviewer reviews with the right frame, and a **"look for" list framed as a floor,
not a gate** so the concern isn't fenced off to just the bullets.

## Types of lens worth having

A good lens set maps onto the things your project actually cares about. Common categories:

- **Language / framework conventions** — idiomatic, safe use of your stack; point at your house style.
- **Architecture & simplicity** — layering, boundaries, over-engineering, missing seams. Usually
  `broad` level — run it before the line-by-line lenses.
- **Testing** — honesty, isolation, coverage of the shapes that actually break.
- **Security** — input handling, authn/z, secrets, injection surface.
- **Compliance / regulatory** — an external standard (PCI, GDPR, an accessibility spec) fetched live.
- **Docs & comments** — restating-the-code and wrong-altitude smells; keeping prose in step with code.
- **Domain / business concerns** — the rules specific to *your* product that no generic tool knows.
- **Ops / observability / cost** — the runtime-and-money angle on a change.

You don't need all of these, and you'll invent ones that aren't here. The point is coverage: **any rule
you care about should be some lens's job to check** — otherwise it lives only in your head and in
repeated prodding.

## Writing a good lens

Full format spec: [`reference/lens-format.md`](reference/lens-format.md). The reviewer's contract:
[`reference/reviewer-brief.md`](reference/reviewer-brief.md). In short:

- **One concern per lens.** If a lens is doing two jobs, split it.
- **Set the context.** Open with who the team is, what you run, and what you *value* — the examples do
  this in a `Context` paragraph. This is where the higher-quality lenses earn their keep: a reviewer
  told "small team, boring code over clever, null-safety is where we get paged" weights findings the way
  you would, instead of applying a generic checklist flat.
- **Make "look for" a floor, not a gate.** List the things that matter *most* and say so — the reviewer
  should also flag anything else that violates the concern, and skip a listed item that doesn't apply.
  Same logic as `triggers`: the list guarantees the important cases aren't missed; it doesn't fence off
  the concern. A closed-sounding checklist quietly narrows the review.
- **Cite, don't paraphrase — when you have a reference.** If the convention is written down (a doc, a
  standard, a URL), list it in the lens body and keep the rest to *what to check*. The reviewer opens
  it and reads the live text, so your lens never goes stale. Only carry the checklist inline when
  there's no canonical source to point at.
- **Phrase the body as things to *find*.** "Flag X", "look for Y" — a checklist the reviewer applies,
  not an essay.
- **Hint a model tier if it matters.** A deterministic grep lens runs fine on a fast, cheap model; an
  architecture lens wants the deepest one. Set `model: fast | standard | deep` and the orchestrator
  sizes the reviewer to the job (omit it and it infers from `level` and shape). Cheap lenses staying
  cheap is part of what makes a big lens set affordable to run.
- **Write a sharp `concern` — it's what gets your lens picked.** In auto mode the orchestrator runs a
  lens whenever its `concern` reads relevant to the change, not only when a trigger fired. A vague
  one-liner gets skipped; a precise one gets run when it should. This is the field that carries
  relevance.
- **Treat `triggers` as a floor, not a gate.** They *guarantee* the obvious path matches aren't missed,
  but the orchestrator adds any lens whose concern fits and skips triggered ones with nothing to
  review. So you don't need to enumerate every path — a good `concern` covers the rest. You can even
  leave triggers off entirely and rely on concern-matching (plus directed requests).
- **Mark `level`.** `broad` (architecture, security-surface, plan-level) runs before `detail`
  (line-by-line), and its findings inform the detailed pass.
- **Calibrate severity in the body.** Say what's blocking vs. a suggestion, so reviewers agree with you.

## How it fits together

```
.review-lenses/             ← your lenses (repo root, you own this)
  architecture.md
  testing.md
  ...

skills/review-lenses/       ← this skill (installed; don't edit to extend)
  SKILL.md                    orchestrator: prose → jobs → dispatch → collate
  reference/
    lens-format.md            the lens file format
    reviewer-brief.md         the read-only reviewer's contract
  examples/                   copy-me starting lenses
```

The orchestrator runs in the main loop (so it can ask you a clarifying question); each reviewer is a
headless, read-only subagent. Reviewers never edit anything — the output is always findings.
