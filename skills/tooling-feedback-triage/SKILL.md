---
name: tooling-feedback-triage
description: Review and act on accumulated feedback reports about agents, skills, and tools — the field reports left by the tooling-feedback skill under .agent-feedback/. Finds the reports, investigates each against the agent, skill, or tool it names, drives it to a resolution, and cleans up handled reports. Defers the actual remedy to the repo's own conventions or to the user — it does not invent fixes. Trigger on "triage feedback", "review agent feedback", "process tooling feedback", "handle the field reports", or a periodic feedback sweep.
---

# Tooling feedback triage

Acts on the field reports recorded by the **tooling-feedback** skill. Each report is about an
**agent**, a **skill**, or a **tool** that fell short — not just tool usage. That skill only
*records*; this one *processes*: it gathers the outstanding reports, works out which are real,
gets each to a resolution, and clears it away.

What it deliberately does **not** do is decide the remedy on its own. The right response to a
report — edit an agent or skill file, open an issue, adjust config, update docs, or judge it not
worth acting on — depends entirely on the project. This skill's job is to **surface, validate,
and route**; the *fix* comes from the repo's conventions or from the user.

## Find the reports

1. **Default location:** `.agent-feedback/`, a directory of per-report markdown files (the
   format tooling-feedback writes). Each has frontmatter (`subject` — the agent, skill, or tool
   the report is about — plus `kind`, `date`, `branch`, and an optional `session`) and a body
   describing what went wrong.
2. **If that directory is absent or empty,** check whether the repo keeps feedback elsewhere —
   a single tracked file, or a path named in `CLAUDE.md` / `AGENTS.md` / contributing docs. A
   quick search for "feedback" across those files usually settles it.
3. **If you still can't find any,** say so and stop — there's nothing to triage. Don't
   manufacture work.

## Process each report

For every report found:

1. **Read it.** If it carries a `session` id and you're on the machine that produced it, you may
   open that transcript for fuller context; otherwise work from the report alone — it's written
   to stand without the session.
2. **Validate against the named subject.** Open the agent, skill, tool, or config the report
   names and check the issue is real and still present — not already fixed, not a one-off
   misread. Reports come from observed failures, so weight them over hypothetical concerns, but
   confirm before acting.
3. **Decide the route — using the repo or the user, not your own invention.**
   - First look for an **established convention**: does the project document how feedback is
     resolved (a fix-the-file pattern for the agent/skill, an issue tracker, a changelog)? If
     so, follow it.
   - Absent a convention, **present your analysis to the user** — the report, whether you think
     it's valid, and a recommended action — and let them direct. Don't autonomously rewrite
     tooling or file issues unless the repo's pattern or the user clearly calls for it.
4. **Carry out the agreed action.**

Work newest-first, or group by `subject` if several reports point at the same agent, skill, or
tool — fixing it once can resolve a cluster.

## Clean up

Once a report has been resolved — fixed, filed, or deliberately dismissed — **delete the file.**
git history preserves the record, so there's no need to archive it. Note what was done (or why
it was dismissed) in the commit message that carries the deletion.

Only delete reports you've actually closed out — leave unresolved ones in place.

Keep this proportionate — triage is a periodic sweep, not a standing process. On a small or solo
project, a short pass that fixes the clear ones, routes the unclear ones to the user, and tidies
up afterwards is the whole job.
