---
name: idiomatic
concern: Anything built with a language, framework, platform or tool. Code, config, build and
 deployment setup, infrastructure. Focuses on whether the approach is the natural, documented one
 for the tools in use, and whether a well-maintained library already does the job.
triggers:
  - "**/*"
level: broad
model: deep
---

# Context

Every ecosystem has its normal way of doing things. ASP.NET, Python, React and Terraform each have
documented patterns, extension points and well-known libraries. Code that follows the ecosystem's
documented patterns is easier to read and easier to hire for. It also gets fixes and security updates
from the people who maintain those tools full time.

Default to the plain, documented path for the context. Leave it only for a good reason, and state the
reason. Prefer a common, well-built, maintained library over writing a new version of it.

This lens relies on judgement. Use your knowledge of the ecosystems involved. The sections below are a
starting point.


# Why this lens exists

AI models often keep the first idea that works and refine it. They rarely step back to ask whether a
cleaner option exists. The result is a growing hand-written solution to a solved problem.

Example: generating safe filenames from user-provided text. One implementation converted accented
characters by hand, one mapping at a time. The AnyAscii library already does this transliteration,
and does it better.

Look above all for hand-written solutions to solved problems. Ask of each part of the target: if
someone started fresh with this problem and these tools, would they build it this way?


# Scope

Start from what the caller asked you to review. Then look at enough of the surrounding project to
know its stack:

- Languages, frameworks and their versions, from the project's own files. Package manifests, lock
  files, project files and toolchain config all say what is in use.
- Dependencies already in use.
- The project's own established conventions.

Check findings against the current official documentation for the version in use. Frameworks change
faster than training data. Do not rely on memory for what a framework provides or recommends.


## Hand-written solutions to solved problems

- Code that reimplements something the framework, standard library or a common library already
  provides. Common cases are parsing, encoding, transliteration, date handling, retries, validation,
  serialisation, caching, authentication, dependency injection, configuration and logging.
- Code that keeps adding special cases, such as a growing lookup table or a new branch for each
  format or edge case. This often means the problem is general and already solved.
- Security-sensitive code written by hand, such as cryptography, auth, sanitising and escaping.
  Treat this as `BLOCKING` when a standard option exists.


## Working against the tools

- Patterns carried over from another ecosystem, when the current ecosystem has its own documented
  pattern for the same job.
- Bypassing a framework's documented extension points.
- Overriding framework defaults with custom code when configuration would work.
- Structure or naming that a reader in this ecosystem would not expect.


## Dependencies

- When suggesting a library, check that it is actively maintained, widely used and suitably
  licensed, and that it fits the stack and version. Link to its docs or package page.
- Prefer something already in the project's dependencies, or in the standard library, over a new
  package.
- Flag a new dependency when the project or standard library already provides the feature. Flag a
  large dependency pulled in for one small function.
- Suggest a dependency. Do not insist on it. Adding one is the owner's decision.


## Deliberate departures

- A departure from the normal path is fine when it has a stated reason, such as performance, a known
  library bug or a platform limit. Check that the reason still holds.
- Flag a departure with no stated reason, and ask for one.
- Following the project's own established convention is fine, even when the wider ecosystem differs.
  If the whole project departs from the ecosystem's norm, raise one broad finding. Do not flag every
  file.


# Findings

Report a list of suggestions, most severe first.

- `what` names the approach taken and the standard alternative.
- `why` cites the official documentation or library page, with a link.
- `fix` names the library, framework feature or pattern to use. It also names the code that the
  change replaces.
- Use `ATTENTION` for a hand-written solution to a solved problem, or for working against the
  framework. Use `SUGGESTION` for smaller idiom choices. Use `BLOCKING` for hand-written
  security-sensitive code where a standard option exists.
- If you cannot tell whether a departure is deliberate, report `UNRESOLVED` and say what you would
  need to know.
- If the approach is idiomatic, say so and stop.
