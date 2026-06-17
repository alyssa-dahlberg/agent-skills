# agent-skills

A collection of [agent skills](https://github.com/vercel-labs/skills) — reusable instructions you can drop into Claude Code and other agents.

## Install

Install every skill in this repo:

```bash
npx skills add alyssa-dahlberg/agent-skills
```

Install a single skill:

```bash
npx skills add alyssa-dahlberg/agent-skills --skill tooling-feedback
```

Target Claude Code specifically:

```bash
npx skills add alyssa-dahlberg/agent-skills -a claude-code
```

> **Skill not showing up after install?** `npx skills` installs into `.agents/skills/` (or
> `~/.agents/skills/`) and is meant to symlink that into `.claude/skills/`, which Claude Code
> scans at startup. That symlink sometimes doesn't get created
> ([#851](https://github.com/vercel-labs/skills/issues/851),
> [#1355](https://github.com/vercel-labs/skills/issues/1355)). If a skill is missing, check that
> `.claude/skills/<name>` exists and link it by hand if not.

## Skills

- **[tooling-feedback](skills/tooling-feedback/SKILL.md)** — capture an in-the-moment field
  report when an agent, skill, or other tool falls short, written as a tracked file under
  `.agent-feedback/` so it travels with the PR and is reviewable in the diff. Recording only.
- **[tooling-feedback-triage](skills/tooling-feedback-triage/SKILL.md)** — the other half: find
  the accumulated reports, validate each against the tool it names, route it to a resolution
  (deferring the actual fix to the repo's conventions or the user), and clean up when done.

## Layout

Each skill is a directory under `skills/` containing a `SKILL.md` with YAML frontmatter
(`name`, `description`) plus any supporting files:

```
skills/
├── tooling-feedback/
│   └── SKILL.md
└── tooling-feedback-triage/
    └── SKILL.md
```
