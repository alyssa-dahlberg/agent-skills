# Lens format

A **lens** is one *concern* to review through — testing, a language's conventions, a compliance
standard, comment quality, architecture, … Lenses are **data, not agents**: each is a small markdown
file the reviewer is handed at review time. The reviewer reads the lens, reads any references the lens
points at, then reviews the target.

Adding a concern is **dropping a file** in `.review-lenses/`. No agent to author, no dispatch table to
edit — the orchestrator discovers lenses from that directory and selects the relevant ones by their
`concern` (with `triggers` as a floor; see below).

**Lenses are independent.** A lens describes *its own* concern and never names or depends on another
lens. When a reviewer notices something outside its lens's concern, it hands that lead back to the
orchestrator (a `HANDOFFS:` note), and the orchestrator decides what else to run from the lenses it
has. So concerns compose through the orchestrator, never by one lens referencing another — that's what
keeps each lens a self-contained, droppable file.

## Format

Frontmatter carries only what the orchestrator needs to *list and select* a lens. Everything else —
including the references — is just prose in the body, because the reviewer reads the whole file.

```markdown
---
name: testing                        # kebab-case; matches the file name
concern: One line — what this lens cares about.
triggers:                            # OPTIONAL — globs; a diff touching these auto-selects the lens
  - "**/*.test.ts"
level: detail                        # broad | detail — a hint for sequencing, not a hard rule
---

Look for: <specific, checkable things>. Cite the reference and section in each finding.

References — the reviewer opens every one before reviewing:
- `CONTRIBUTING.md#testing`              (local path — read from the working tree)
- https://example.com/some-standard      (URL — fetched at review time)
```

## The fields

- **`name`** — kebab-case, matching the file name. A stable label for the lens in reports and directed
  requests ("review the `testing` lens on X"). Selection runs off `concern`/`triggers`, not `name`, so
  its only job is to be a readable identifier — keep it in sync with the filename.
- **`concern`** — one line; also what the orchestrator shows when it lists which lenses it ran.
- **`triggers`** — *optional*. A **starting point** for auto-selection, not a gate. In *auto* mode
  ("review this branch") a lens whose globs match a changed path is definitely run — but the
  orchestrator *also* runs any lens whose `concern` reads relevant to the change even if no glob fired,
  and may skip a triggered lens with nothing to review. So `concern` carries the real selection
  signal; `triggers` just guarantees the obvious matches aren't missed. A lens with narrow or no
  triggers still gets picked up when its concern fits (and is always available for a directed request).
  Keep triggers honest: they're the floor, not the ceiling.
- **`level`** — `broad` (architecture, security-surface, plan-level) runs before `detail`
  (line-by-line) so higher-level findings inform the detailed pass. A sequencing hint.
- **`model`** — *optional*. How much horsepower the reviewer needs, as a tier: **`fast`** (a cheap,
  quick model — right for deterministic/scripted lenses like a grep sweep), **`standard`** (the
  default), or **`deep`** (the most capable model — right for architecture, security-surface, or
  anything that needs real understanding). The orchestrator maps the tier to the host's actual models
  and passes it when dispatching this lens. Omit it and the orchestrator infers from `level` and the
  lens's shape. You may name a concrete model instead of a tier if you want to pin one — at the cost of
  portability across harnesses and model generations.

## Writing the body

The body is what the reviewer actually reviews against. A bare list of bullets works, but the good
lenses do two more things — see the [`examples/`](../examples/), which open with a `Context` paragraph
and frame their checklist as a floor:

- **Set context.** Tell the reviewer who the team is, what they run, and what they *value* — small team
  vs. large, the stack, "boring code over clever," which failure modes have actually hurt in production.
  This frame is what turns a generic checklist into a review that knows what lands hard *here* and what's
  noise. A reviewer handed context weights findings the way you would.
- **Make the checklist a floor, not a gate.** Phrase "look for" as the things that matter *most*, and
  say so explicitly — the reviewer should also flag anything else that violates the concern, and skip a
  listed item that doesn't apply. A closed checklist reads as "only these"; you want "these, and use
  judgement on the rest." Same floor-not-ceiling logic as `triggers`: the list guarantees the important
  cases aren't missed, it doesn't fence off the concern.

## References live in the body, not the frontmatter

A lens's **references** are its source of truth for the convention — a local doc, a style guide, an
RFC, a compliance standard. Put them in the body as bullets or inline links; there's no structured
field, because the reviewer reads the whole lens and opens whatever it points at. Each reference is a
**local path** (read from the working tree) or a **URL** (fetched at review time).

- **If a lens has references, don't paraphrase them** — point at them and say what to check. The
  reviewer reads the live text, so findings never drift from a copy that goes stale.
- **If a lens has no references, the body is self-contained** — it carries the full checklist inline.
  Fine for a widely-agreed best practice with no single doc to cite.

## Two shapes, one format

There's no "starter vs. real" split — just whether a lens points at references:

- **Reference-backed** — cites local docs and/or URLs; body stays thin and says what to check. Best
  once your conventions are written down somewhere, or when checking against an external standard.
- **Self-contained** — no references; body carries the full checklist. Best for a universal
  best-practice concern (comment quality, simplicity) with no canonical doc to cite.

A lens can start self-contained and later grow a references section pointing at your own docs as your
conventions solidify — the reviewer handles both the same way.
