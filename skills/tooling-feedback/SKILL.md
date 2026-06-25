---
name: tooling-feedback
description: Capture an in-the-moment field report when an agent, skill, or tool falls short during a real session — a missed catch, awkward steps, a wrong trigger, or just leaving you wishing it did more. Covers all three — the agents you delegate to, the skills you invoke, and the tools you call — not just tool usage. Writes a small tracked file under .agent-feedback/ so the report travels with the PR and is reviewable in the diff. Trigger whenever any of them underperforms mid-task (don't break flow to do it), or whenever the user explicitly asks to log feedback — phrases like "tooling feedback", "agent feedback", "skill feedback", "log feedback", or "file a field report".
---

# Tooling feedback

Field reports about where an **agent, skill, or tool** could be better — captured *in the
moment*, during real work, when one falls short. The point is to turn a fleeting "that was
awkward" into a durable, reviewable signal without derailing the task.

"Tooling" here is deliberately broad. It is **not** only about tool calls — it covers all three
kinds of thing you work through:

- **agents** — a subagent you delegated to that did the wrong thing or missed something
- **skills** — a skill that triggered badly, gave awkward steps, or fell short
- **tools** — a tool or command that behaved unexpectedly or got used wrongly

A report can also be about *the agent itself* — your own behaviour in the session.

Unlike a scratch backlog, each report is **checked in with the PR it came from**. That makes
it portable (no machine-local session links that die when the transcript is gone) and puts it
in front of whoever reviews the change.

## When to capture

Log a report the moment an agent, skill, or tool underperforms:

- it **missed** something it should have caught
- it gave **awkward or wrong steps**
- it **triggered when it shouldn't have**, or failed to trigger when it should
- it left you **wishing it did more**

Also capture whenever the **user explicitly asks** — e.g. "tooling feedback", "agent feedback",
"skill feedback", "log feedback", "file a field report". Treat that as a direct request to
write a report now.

If you're unsure it's worth it, log it anyway — these files are cheap and lost signal isn't.

Logging should not derail the user, but the **report itself should be thorough**. You have the
full session in context right now; the person triaging this later will not — they'll have only
this file and the PR. Spend that context generously: write down what you were doing, how you
got here, and what actually went wrong while you still remember it. A rich report is cheap for
you to write now and expensive to reconstruct later.

## How to capture

1. Pick a slug for the agent, skill, or tool that fell short (its name, kebab-cased) — e.g.
   `server-reviewer` (an agent), `ship` (a skill), `bash-git-push` (a tool), or
   `the-agent-itself`.
2. Write a new file at `.agent-feedback/<YYYY-MM-DD>-<slug>.md`. One report per file — never
   append to an existing one (that's what reintroduces merge conflicts). If a file with that
   name already exists, add a short suffix: `-2`, `-b`, etc.
3. Use this shape. Fill every section you can from what's in context — omit one only if it
   genuinely doesn't apply:

   ```markdown
   ---
   subject: server-reviewer
   kind: agent
   date: 2026-06-15
   branch: feature/image-upload
   session: 0c4f2a82-1e7b-4774-bec8-b8656d3c8ca6
   ---

   **What I was doing:** the task in progress and why this agent/skill/tool came into play —
   the goal, the command or request that triggered it, and where in the work it happened.

   **What led here:** the relevant steps that came before — what was tried, what it was given
   to work with, any earlier results that set up the failure. Enough trail that the reader can
   see how you arrived at the problem.

   **What went wrong:** concretely what it did or didn't do — the missed catch, the wrong step,
   the bad trigger. Quote the specific output, file, or path involved where it helps.

   **What would've been better:** the concrete change that would have helped — a check to add,
   a step to reword, a trigger to tighten. The most actionable part for triage.

   **User notes:** anything the user adds in their own words. Omit if they don't.
   ```

   `subject` names the thing the report is about; `kind` says which sort it is — `agent`,
   `skill`, or `tool` — so triage can group and route. The `session` field is the current
   session id. In Claude Code, write the literal token
   `${CLAUDE_SESSION_ID}` as the value — it's substituted with the real id when the skill loads.
   On other agents use their equivalent (or the `$CLAUDE_CODE_SESSION_ID` environment variable),
   and omit the field if there is none. It's a *local* deep-link back to the full transcript:
   useful for triage on the same machine, harmless when it's not. Because it may be dead, the
   written report above must stand on its own without it.

4. **If the user offered feedback in their own words, capture it** under *User notes* — verbatim
   or lightly tidied, not reworded into your own framing. If they triggered this without saying
   much, a quick "anything you'd add?" is fine, but don't block on it.

5. **Stage it with your change** so it lands in the same PR (`git add .agent-feedback/...`).
   The PR is the context — the reviewer sees the report alongside the diff that provoked it.

Identify the agent, skill, or tool — not a person. Keep each report self-contained: assume the
reader has only the file and the PR, not your session.

This skill only **records** reports — it does not triage them. Acting on the accumulated
reports under `.agent-feedback/` is a separate concern (and a separate skill).
