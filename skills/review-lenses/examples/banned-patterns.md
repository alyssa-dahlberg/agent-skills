---
name: banned-patterns
concern: Fast deterministic sweep for patterns that are always wrong in this codebase — run the greps, every hit is a finding unless justified inline.
triggers:
  - "**/*"
level: detail
model: fast   # deterministic greps + a light sanity-filter — no deep reasoning needed, so run it cheap
---

> **This is an example lens of a different shape: prescriptive and scripted.** Instead of asking the
> reviewer to judge, it hands over exact commands to run and a rule for what a hit means. Deterministic
> checks like these are the cheapest, most reliable findings you can get — they don't drift and they
> don't hallucinate. Use this shape for the handful of patterns that are *unambiguously* wrong in your
> repo; leave the judgement calls to other lenses. Tune the pattern list to your stack.

**Context.** Some mistakes aren't worth anyone's judgement — they're just banned, and a grep finds them
faster and more reliably than reading ever will. This lens *is* that grep. Every match is a finding
unless the line carries an explicit inline waiver (e.g. a trailing `banned-ok: <reason>` marker you've
agreed on). Run each check over the target, scoping to the changed files for a branch review. Report
every hit as `file:line` with the pattern it matched and the fix.

**Focused / skipped tests left in** — these silently switch off coverage:
```bash
rg -n --pcre2 '\b(fit|fdescribe|xit|xdescribe)\b|\.(only|skip)\s*\('
```
BLOCKING — a committed `.only` means most of the suite isn't running in CI.

**Debug leftovers in shipped code** (exclude tests):
```bash
rg -n 'debugger|console\.(log|debug|trace)|System\.out\.println|Console\.WriteLine|binding\.pry' \
  -g '!**/*test*' -g '!**/*spec*'
```
ATTENTION — a stray debug print in production code.

**Committed merge-conflict markers:**
```bash
rg -n '^(<<<<<<<|>>>>>>>) '
```
BLOCKING — an unresolved conflict got committed. (Match the `<<<<<<< ` / `>>>>>>> ` markers, which
carry a trailing ref name; the bare `=======` divider is skipped because it collides with a Markdown
setext heading underline — the two angle-bracket markers still catch every real conflict.)

**Hardcoded secrets (heuristic):**
```bash
rg -ni --pcre2 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----|(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*\S{6,}'
```
BLOCKING on a real match — but verify first: filter out env-var reads (`= process.env.X`), obvious
placeholders (`changeme`, `xxxx`), and test fixtures before you flag.

**TODO/FIXME with no owner** — a TODO nobody owns never gets done:
```bash
rg -n --pcre2 '\b(TODO|FIXME|HACK|XXX)\b(?!\()'
```
SUGGESTION — flags every marker except the owned `TODO(name)` form (so `TODO: clean up` *is* flagged,
`TODO(alice)` is not). If your convention allows a ticket reference instead of an owner, filter those
out by eye.

**This list is a floor.** Add your own — a deprecated API you're migrating off, a config key that must
never be committed, a banned import, an Americanism in user-facing copy. Each is one `rg` line plus a
severity. And if you spot a clearly-banned pattern that isn't scripted here, flag it anyway and suggest
adding a check for it.
