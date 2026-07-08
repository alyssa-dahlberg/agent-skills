---
name: review-lenses
description: Review code, a plan, a design, or an idea through one or more lenses. Accepts plain-English requests — "review this branch", "review the architecture of these interfaces", "check the payment flow against PCI concerns", "sanity-check this idea". Resolves the request into review jobs (each one lens × one target), dispatches read-only reviewers, and collates one report. A lens is a small markdown file in .review-lenses/ describing one concern; adding a concern is dropping a file. Use whenever the user or a calling agent asks to review, check, or sanity-check anything — and reach for it proactively — any agent can and should self-serve a review of its own work before handing it over (before finalizing a change, after anything security-sensitive, when unsure). It's cheap, read-only, and you don't need to be asked.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - Agent            # the subagent-dispatch tool; named Task on some Claude Code builds
  - Task             # listed alongside Agent so dispatch works whichever name the host uses
  - WebFetch
  - WebSearch
  - AskUserQuestion
---

# Review lenses

You are the **review orchestrator**. You are the brain; the reviewers are headless workers. Your job:
turn a request (prose) into a **review plan** — a set of jobs, each one **(lens × target)** — dispatch
them, and collate one report.

**Review is self-serve.** This skill isn't only for when a human types a review request — any agent
should invoke it on its *own* work before handing it back: before finalizing a change, after anything
security-sensitive, whenever unsure. It's cheap and read-only, and the report comes back structured so
a calling agent can act on the findings directly. Reach for it proactively; you don't need to be asked.

Two axes, kept independent: a **lens** = *what to look for* (a file in `.review-lenses/`); a **target**
= *what to look at* (a diff, a class, a plan phase, a whole plan, a design doc, an idea). Any lens
applies to any target. A **job** is one lens on one target. See [reference/lens-format.md](reference/lens-format.md)
for the lens file format and [reference/reviewer-brief.md](reference/reviewer-brief.md) for the brief you
hand each reviewer.

## Step 1 — Resolve the request into a plan

Read the request and produce `{ jobs: [{lens, target, context, level}], mode }`. You clarify here
because reviewers can't — they run headless. Only ask when genuinely ambiguous; otherwise infer and
proceed (use `AskUserQuestion` for real forks like "phase 3 — the evaluator or the migration?").
`AskUserQuestion` only works when you're the main-loop agent — if this skill was invoked from inside a
subagent (an agent self-reviewing its work), infer and proceed, leaning on `UNRESOLVED` findings for
anything you can't settle.

**Find the lenses.** The lens directory is `$REVIEW_LENSES_DIR` if that environment variable is set,
otherwise `.review-lenses/` at the repo root:
```bash
echo "${REVIEW_LENSES_DIR:-.review-lenses}"
```
`REVIEW_LENSES_DIR` lets a project point at a custom location; how you set an env var depends on your
harness (e.g. in Claude Code, add it to `.claude/settings.json` under `"env"`). Read the frontmatter of
every `*.md` in that directory **except `README.md`** — take `concern`, `triggers`, `level`. If no lens
directory exists yet, say so and point the user at the examples shipped with this skill.
- *Directed* request ("review the testing of X") → the named lens(es), regardless of triggers.
- *Auto* request ("review this branch") → **triggers are a starting point, not the whole selection.**
  Do two passes:
  1. **Triggers matched → run it.** Any lens whose `triggers` globs match a changed path is in — that's
     the floor.
  2. **Concern reads relevant → also run it.** Go through the *rest* of the lenses and read each one's
     `concern`; if a lens's concern is clearly relevant to this change even though no glob fired, add
     it. `concern` is what you judge relevance on — a lens with narrow or no `triggers` still applies
     when its concern fits. Some concerns (comment quality, simplicity) apply to *any* code-bearing
     diff — include them whenever code changed.

  You may also **skip** a triggered lens that plainly has nothing to review here. Triggers are cheap
  path-matching; your judgement on `concern` is the real selection. **Say which lenses you added or
  dropped by judgement** so coverage stays transparent.

**Scope the target.** Infer *what's under review* from the request — a class/symbol, a plan phase, a
design doc, a speculative idea, or a diff. For "review this branch" the default target is **this
branch's own changes including uncommitted work**. Diff against the **merge-base** with the integration
branch — detect that branch (don't assume `main`; it may be `master`, `trunk`, or an `upstream` remote),
and diff two-dot from the merge-base so uncommitted work is included and the base branch's own newer
commits are excluded:
```bash
# integration branch = the remote's default; fall back to origin/main, then a local main/master
BASE_REF=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null \
  || for b in origin/main origin/master main master; do git rev-parse --verify --quiet "$b" >/dev/null && echo "$b" && break; done)
BASE=$(git merge-base "$BASE_REF" HEAD)
{ git diff --name-only "$BASE"; git ls-files --others --exclude-standard; } | sort -u
```
If the target is empty (e.g. an empty diff), say so and stop.

**Context.** If a half-built feature is under review, findings go wrong without the intent behind it.
So pass along any context the caller supplies (research just done, a test just run green), and if the
caller names or you can spot a governing planning/design doc for the change, pass its path as context
too. The reviewer is told how to read it: trust statements of *intent/scope*, verify *claims of done*.

**Level & mode.** Tag each job `broad` (architecture, security-surface, plan-level) or `detail`
(line-by-line) from the lens's `level`. **Mode** is `focused` (one/few jobs, no sequencing) for a
narrow directed ask, or `full` (phased by level) for a branch review.

**Proportionality — do less by default.** A small focused ask is a single job; don't inflate it. Only
compose extra levels/jobs when signals justify it (a whole feature is in play, or depth was asked
for). Running a multi-lens whole-plan review on a two-line diff is exactly the ceremony to avoid.

## Step 2 — Dispatch

Run **broad-level jobs first**, then **detail-level jobs briefed with the broad findings** (if the
approach is wrong, line-by-line nits on that code are moot). Within a level, dispatch in parallel
(reviewers are read-only, no conflicts).

For each job, spawn a **read-only** subagent that can **read files and fetch URLs** — it needs
`Read`/`Glob`/`Grep`, read-only `Bash`, *and* `WebFetch`/`WebSearch`, because a reference-backed lens
may cite online references (a standard, an RFC, a compliance doc) the reviewer must open at review
time. In Claude Code the `Explore` agent type fits (read-only, with web access); a dedicated reviewer
agent the repo ships works too; otherwise use a general-purpose agent instructed to stay read-only.
**Don't dispatch a reviewer to a lens with URL references on an agent type that lacks web tools** — it
would silently fall back to reviewing from memory, the exact drift this design avoids.

**Size the model to the job.** The dispatch tool takes a `model` parameter — use it. If the lens sets a
`model` hint, honour it, mapping the tier to the host's models: `fast` → the cheapest/quickest, `deep` →
the most capable, `standard` → the default. If the lens gives no hint, infer: a `broad`-level or
understanding-heavy lens (architecture, security-surface, a design/plan target) wants the strongest
model; a deterministic or scripted lens (a grep sweep like `banned-patterns`) runs fine on the
cheapest, fastest one; everything else takes the default. Matching model to job is what keeps a big lens
set affordable — don't pay top-tier rates to run a ripgrep, and don't review architecture on a small
model.

Give it the full contents of [reference/reviewer-brief.md](reference/reviewer-brief.md) plus:
- the **lens file path**, the **target** (and how to obtain it — the diff range, the file, the plan
  phase), the **context** (any plan path + notes), the **level**, and any broad-level findings to build on.

## Step 3 — Loop if a lead warrants it (don't one-shot)

The plan is grown, not fixed. After results, you may append jobs — but bounded:
- **Deepen** a confirmed-but-shallow finding (does the pattern recur elsewhere? blast radius?).
- **Verify** a plausible-but-uncertain finding before it enters the report. Spawn an **independent**
  job — a fresh reviewer, briefed to *try to refute* — and have it return a verdict on this ladder:
  - **CONFIRMED** — it can name the inputs/state that trigger the problem and the concrete wrong
    outcome, and quote the line. Ship it.
  - **PLAUSIBLE** — the mechanism is real but the trigger is uncertain (timing, env, config). Ship it,
    marked needs-confirmation. **Plausible by default:** don't refute something merely for being
    "speculative" when the state is realistic — a race, a nil on a rare-but-reachable path (error
    handler, cold cache, missing optional field), a falsy-zero treated as missing, a boundary
    off-by-one, a retry storm, a regex that lost an anchor.
  - **REFUTED** — factually wrong (the code doesn't say that), provably impossible, or already handled
    elsewhere in the change; quote the line that proves it. Drop it.

  Only **REFUTED** removes a finding — CONFIRMED and PLAUSIBLE both make the report (PLAUSIBLE flagged
  as such). This keeps confident-but-wrong findings out without silencing real-but-uncertain ones.
- **Route** a cross-concern handoff. A reviewer running one lens may flag something outside its concern
  (a `HANDOFFS:` line — "spotted what looks like a secret while reviewing architecture; needs a
  security pass"). Lenses are independent and never call each other — *you* are the router. **Handoffs
  are suggestions, not commands.** Use judgement:
  - If the concern is **already covered** — that lens already ran (or is queued) over the same target,
    or the lead is already captured in a finding — **don't re-run it.** Note it's covered and move on.
  - If it's **not covered and a lens fits**, dispatch that lens on the relevant target.
  - If **no lens claims the concern**, surface it as an `UNRESOLVED`/suggestion and note the gap (maybe
    a lens should exist).

  This is the broad→detail loop widening sideways: a finding in one concern *can* open a job in
  another — only when it adds coverage you don't already have.

**Stopping rule:** stop when there are no new leads, the lead is confirmed/refuted, or you've done a
round or two of depth. If you stop while a thread is open, **say so** ("didn't chase X further —
flagging for a human"). A good reviewer follows a thread; it doesn't crawl forever.

## Step 4 — Collate one report

Merge all findings into a single report, **grouped by level (altitude) → lens (concern) → severity**.
A plan-level "drifts from the design" and a diff-level "no test here" are different kinds of thing;
don't flatten them into one list. Dedup findings raised by more than one job; name the source lens on
each.

Structure:
1. **Verdict** — one line: safe to ship / needs attention / blocking issues present. (For non-code
   targets: sound / has gaps / has serious problems.)
2. **Blocking** 🚨, **Attention** ⚠️, **Suggestions** 💡 — findings, source lens named, `file:line`
   where it's code.
3. **Unresolved** ❓ — things a reviewer couldn't determine; ask the user, and if the answer matters,
   re-dispatch that one job with it added to context.
4. **Jobs run** — the lenses dispatched, for coverage transparency.

**Where the report goes:** by default keep it transient — the session scratchpad — and always return
the findings in your reply so a calling agent can act on them without opening a file. If the review is
tied to a planning/design doc the caller named, you may write the report beside it so findings are
ticked off in place; don't edit the plan itself silently.
