---
name: testing
concern: Test honesty, isolation, and coverage discipline — do the tests exercise the real thing, and do they cover the shapes that actually break?
triggers:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/*_test.*"
  - "**/test/**"
  - "**/tests/**"
level: detail
---

> **This is an example lens**, and a **self-contained** one: it cites no references, so the body is the
> whole spec — right for a widely-agreed concern with no single canonical doc to point at. The *Context*
> paragraph is invented to show how a lens carries a team's actual testing philosophy; replace it with
> yours. Once you write your testing standard down, add a references list pointing at it and thin this
> body accordingly.

**Context.** We've been burned by tests that were green and lying — mocked-out dependencies that let a
broken integration ship — so our house rule is **test against the real boundary**: real database via
throwaway containers, real HTTP pipeline in-process, mocks reserved for things we genuinely can't run
(a third-party payment API, the clock). We run everything in parallel, so **isolation is non-negotiable**
— a test that needs a reset step or fails when run twice is a defect in the test. We care more about
covering the **failure and boundary paths** than padding line coverage on the happy path; a test that
can't fail is worse than no test because it buys false confidence. Tests are **part of done**, not a
follow-up ticket.

**Look for the following — a *floor, not a gate*.** These are the failure modes we hit most; also flag
anything else that undermines test honesty, isolation, or meaningful coverage, and skip a listed item
that doesn't apply to the change.

- **Dishonest tests.** A test that exercises a mock or in-memory substitute where the real dependency is
  the thing under test — logic mocked out so the test passes even when the real path is broken.
  Integration-shaped behaviour verified against a fake instead of the real boundary. This is the one we
  care about most: it's exactly the "green and lying" failure the context calls out.
- **Assertions that can't fail.** No assertion at all; asserting on a mock's own return value; a
  snapshot regenerated to match whatever the code did; `assert(true)`-shaped filler. Apply the test:
  *would this fail if I broke the code it covers?* If not, it's not a test.
- **Broken isolation.** Tests sharing mutable state, depending on execution order, or leaking state
  between runs; anything needing a manual reset or a "run it once" caveat. They must be parallel-safe
  and independent.
- **Missing coverage on the risky shapes.** New branching logic, error/failure paths, and boundary
  conditions (empty, null, max, concurrent, retried) with no test. A happy-path-only test on code whose
  whole point is the edge cases is a gap — name the uncovered case.
- **Testing implementation, not behaviour.** Tests coupled to private internals that break on any
  refactor without catching a real regression — over-specified mocks, asserting call order that doesn't
  matter, reaching into private state.
- **New behaviour shipped with no test at all.** A new code path with zero coverage is a finding —
  unless the context says tests land in a named later step, in which case trust that and don't re-flag.
