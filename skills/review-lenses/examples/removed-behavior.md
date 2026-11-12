---
name: removed-behavior
concern: Deletions that silently drop a guarantee — a guard, error path, validation, or test removed without the behavior being re-established.
triggers:
  - "**/*"
level: detail
model: standard   # tracing whether a dropped guarantee is re-established elsewhere
---

> **This is an example lens** — self-contained, and the kind most hand-written lens sets miss.
> Reviewers instinctively scrutinise the lines a change *adds*; this lens points them at the lines it
> *removes*, where a quietly-dropped guarantee hides. It's generic across languages — keep it close to
> as-is.

**Context.** The dangerous change is often not the code that was added — it's the line that was
*removed* and never replaced. A deleted null-check, a narrowed validation, a dropped `catch`, a test
someone deleted "because it was failing": each takes away a guarantee the code used to make, and
nothing in the new code announces the gap. So this lens reviews the diff **from the deletions outward.**

Get the diff and read every line it **removes or replaces** (the `-` side), not just the additions. For
each deletion, the core move is: **name the invariant that line enforced, then find where the new code
re-establishes it.** If you can't find it, the guarantee was dropped — flag it with the concrete
scenario it now breaks.

**Look for the following — a *floor, not a gate*.** Flag any dropped guarantee, not only these shapes.

- **Removed guard or check.** A null/bounds/permission/precondition check that's gone. Name the input
  that now slips through unchecked.
- **Dropped error handling.** A `catch`, error return, retry, or rollback removed. What happens now on
  the failure it used to handle? Silent success and data loss are the usual outcomes.
- **Narrowed validation.** Input validation, a type constraint, or an allowlist/regex made more
  permissive — an anchor lost, a case removed. What does it now accept that it used to reject?
- **Deleted or weakened test.** A test removed, `skip`ped, or gutted of its assertions. Which real case
  was it covering, and is that case still covered somewhere? A test deleted because it "was failing" is
  a red flag, not a cleanup — the failure may have been real.
- **Removed invariant on shared state.** A lock, an ordering step, an idempotency key, or a transaction
  boundary taken out — the kind of guarantee whose absence only bites under concurrency or retry.

Deliberate removals are fine **when the context says so** — a feature being retired, a check moved
somewhere the context names. Trust that, but still verify the guarantee isn't relied on elsewhere
(grep for other callers before you accept it's safe to drop).
