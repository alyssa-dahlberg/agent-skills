#!/usr/bin/env python3
"""Measure whether a skill's description makes Claude reach for it.

Installs the skill under test into a throwaway project, runs each eval query
through `claude -p`, and records whether the run called the Skill tool naming
it. Nothing touches the real repo.

    ./trigger_eval.py --selftest          # prove the harness can detect a trigger
    ./trigger_eval.py                     # run trigger-evals.json against SKILL.md
    ./trigger_eval.py --description "..."  # score a candidate description

Run --selftest first, every time. A harness that cannot detect a trigger
reports zero for a good description and zero for a bad one, and the two are
indistinguishable in the output. That has already happened once here; see
DESIGN.md, "Trigger accuracy is unmeasured".

Why this exists rather than skill-creator's run_eval.py: that harness registers
the skill under test by writing into `.claude/commands/`, which produces a slash
command. Slash commands are listed to the model separately from skills and are
invoked by the user, not chosen by the model, so the Skill tool call it watches
for can never happen. Every query scores false, positives and negatives alike.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent

# A skill the model cannot satisfy from general knowledge, so the only route to
# an answer is the skill itself. A control that the model can answer directly
# proves nothing: it will answer and skip the skill, which looks like failure.
SELFTEST_NAME = "fernwood-release-checklist"
SELFTEST_DESCRIPTION = (
    "Runs the Fernwood release checklist, an internal pre-deploy procedure for this "
    "project covering version stamping, changelog rotation and the canary gate. Use "
    "whenever the user asks to cut a release, prepare a deploy, or mentions the "
    "Fernwood checklist."
)
SELFTEST_QUERY = "i need to cut a release for this project, walk me through the fernwood checklist"


def parse_frontmatter(skill_md: Path) -> tuple[str, str]:
    """Pull name and description out of a SKILL.md. Frontmatter only."""
    text = skill_md.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{skill_md} has no frontmatter")
    fm = text.split("---", 2)[1]
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not desc:
        raise SystemExit(f"{skill_md} frontmatter is missing name or description")
    return name.group(1).strip(), desc.group(1).strip()


def referenced_paths(queries: list[str]) -> set[str]:
    """File paths mentioned in the eval queries.

    The queries name real-looking files ("apps/payments/README.md"). In an empty
    directory the run finds nothing there and may answer "that file doesn't
    exist" without ever considering the skill, which scores as a miss the
    description didn't cause. Seeding empty files removes that confound.
    """
    pattern = re.compile(r"\b[\w.-]+(?:/[\w.-]+)*\.(?:md|cs|json|ya?ml|txt)\b")
    return {m for q in queries for m in pattern.findall(q)}


# Seeded files need real prose in them. Empty or one-line placeholders make every
# query a hunt: the run reads the file, finds nothing to edit, and spends its turn
# establishing that the project is empty. In the first run of this harness all ten
# positives did exactly that and scored 0/10, which said nothing about the
# description. The content need not match what the query claims about it; it needs
# to be long enough and poor enough that editing it is a real task.
SEED_PROSE = """# Overview

This module is responsible for handling the processing of incoming requests in a
way that is robust and scalable. It leverages a number of underlying components in
order to facilitate the delivery of a seamless experience for consumers of the API.

## Getting started

In order to get started, you will first need to ensure that you have the necessary
prerequisites installed. Once that has been completed, the setup process is fairly
straightforward and should not take very long.

The configuration is loaded from the settings file, which contains a number of
options that can be adjusted as needed. The timeout is set to 30 seconds by default,
the retry count is three, and the cache holds 10,000 entries.

## Architecture

Requests arrive at the API layer, which validates them and then publishes them to
the queue. The worker consumes from the queue and writes the results to the store.
Failures are sent to a dead letter queue for later inspection. The retry policy uses
exponential backoff with 20% jitter.

## Notes

It is worth noting that this component was designed with extensibility in mind, and
as such it should be relatively easy to add new functionality going forward. If you
have any questions, please reach out to the team.
"""


def build_project(root: Path, name: str, description: str, seed_paths: set[str]) -> None:
    """Lay out a throwaway project with the skill installed and the query paths present."""
    skill_home = root / ".claude" / "skills" / name
    skill_home.mkdir(parents=True, exist_ok=True)
    # A stub body on purpose. Triggering is decided from the name and
    # description, which is all the model sees before it calls Skill, so the
    # real body would only add tokens and slow every query down.
    (skill_home / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\nStub body for trigger evaluation.\n"
    )
    for rel in seed_paths:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(SEED_PROSE)


def ran_skill(stream: str, name: str) -> tuple[bool, list[str]]:
    """Did this run call Skill on `name`, and what did it call instead?

    Scans the whole run. An earlier harness returned false as soon as it saw any
    tool that was not Skill or Read, so a run that opened with Glob or TodoWrite
    scored as a miss even when it called the skill immediately afterwards.
    """
    tools: list[str] = []
    fired = False
    for line in stream.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant":
            continue
        for item in event.get("message", {}).get("content", []):
            if item.get("type") != "tool_use":
                continue
            tool = item.get("name", "")
            tools.append(tool)
            if tool == "Skill" and item.get("input", {}).get("skill", "") == name:
                fired = True
    return fired, tools


def run_query(query: str, name: str, description: str, seed_paths: set[str],
              timeout: int, model: str | None) -> dict:
    """One query, in its own throwaway project."""
    root = Path(tempfile.mkdtemp(prefix="trigger-eval-"))
    try:
        build_project(root, name, description, seed_paths)
        cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose"]
        if model:
            cmd += ["--model", model]
        # CLAUDECODE is a guard against nesting an interactive session; a
        # subprocess run is safe and has to clear it to start at all.
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        try:
            done = subprocess.run(
                cmd, cwd=root, env=env, stdin=subprocess.DEVNULL,
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return {"query": query, "triggered": False, "tools": [], "error": "timeout"}
        fired, tools = ran_skill(done.stdout, name)
        return {"query": query, "triggered": fired, "tools": tools}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def selftest(timeout: int, model: str | None) -> bool:
    print("Self-test: a skill the model cannot answer without, on a query that needs it.")
    result = run_query(SELFTEST_QUERY, SELFTEST_NAME, SELFTEST_DESCRIPTION, set(), timeout, model)
    if result["triggered"]:
        print("  PASS - harness detects a trigger. Scores below mean something.\n")
        return True
    print(f"  FAIL - control did not fire. Tools called: {result['tools'] or 'none'}")
    print("  Every score this run produces would be zero for reasons that have")
    print("  nothing to do with the description. Fix the harness before reading them.\n")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eval-set", default=str(HERE / "trigger-evals.json"))
    ap.add_argument("--skill", default=str(SKILL_DIR / "SKILL.md"))
    ap.add_argument("--description", default=None, help="score this instead of the one in SKILL.md")
    ap.add_argument("--runs", type=int, default=3, help="runs per query; triggering is not deterministic")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--model", default=None)
    ap.add_argument("--selftest", action="store_true", help="run only the control")
    ap.add_argument("--skip-selftest", action="store_true", help="not advised; see module docstring")
    ap.add_argument("--json", default=None, help="write full results here")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest(args.timeout, args.model) else 1
    if not args.skip_selftest and not selftest(args.timeout, args.model):
        return 1

    name, description = parse_frontmatter(Path(args.skill))
    description = args.description or description
    eval_set = json.loads(Path(args.eval_set).read_text())
    seeds = referenced_paths([item["query"] for item in eval_set])

    print(f"Skill: {name}")
    print(f"Description ({len(description)} chars): {description[:100]}...")
    print(f"{len(eval_set)} queries x {args.runs} runs\n")

    jobs = [(item, run_idx) for item in eval_set for run_idx in range(args.runs)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        outcomes = list(pool.map(
            lambda job: (job[0], run_query(job[0]["query"], name, description, seeds, args.timeout, args.model)),
            jobs,
        ))

    by_query: dict[str, dict] = {}
    for item, outcome in outcomes:
        entry = by_query.setdefault(item["query"], {
            "query": item["query"], "should_trigger": item["should_trigger"],
            "fired": 0, "runs": 0, "tools": [],
        })
        entry["fired"] += int(outcome["triggered"])
        entry["runs"] += 1
        entry["tools"].extend(outcome["tools"])

    results = []
    for entry in by_query.values():
        rate = entry["fired"] / entry["runs"]
        # Majority of runs, so a single flaky run neither passes nor fails a query.
        entry["passed"] = (rate >= 0.5) if entry["should_trigger"] else (rate < 0.5)
        entry["rate"] = rate
        results.append(entry)

    positives = [r for r in results if r["should_trigger"]]
    negatives = [r for r in results if not r["should_trigger"]]
    for label, group in (("SHOULD TRIGGER", positives), ("SHOULD NOT TRIGGER", negatives)):
        print(f"{label}")
        for r in sorted(group, key=lambda r: r["rate"], reverse=True):
            mark = "ok  " if r["passed"] else "MISS"
            print(f"  {mark} {r['fired']}/{r['runs']}  {r['query'][:78]}")
        print()

    recall = sum(r["passed"] for r in positives) / len(positives) if positives else 0
    precision = sum(r["passed"] for r in negatives) / len(negatives) if negatives else 0
    print(f"Fires when it should:     {sum(r['passed'] for r in positives)}/{len(positives)}  ({recall:.0%})")
    print(f"Stays out when it should: {sum(r['passed'] for r in negatives)}/{len(negatives)}  ({precision:.0%})")

    if args.json:
        Path(args.json).write_text(json.dumps({"description": description, "results": results}, indent=2))
        print(f"\nFull results: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
