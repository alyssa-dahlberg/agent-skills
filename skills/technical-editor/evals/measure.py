#!/usr/bin/env python3
"""Objective prose-tell measures. Not a verdict — evidence to read alongside the text."""
import re, sys, statistics, pathlib

TELLS = {
    "manufactured antithesis": r"\b(not just|isn't just|is not just|not merely|rather than merely)\b",
    "not-X-but-Y pivot": r"(It's not |This isn't |That's not )[^.]{3,60}\. It'?s ",
    "emphasis crutch": r"\b(genuinely|fundamentally|truly|actually|simply|critically|load-bearing|at its core)\b",
    "style word": r"\b(delve|tapestry|landscape|realm|seamless|robust|crucial|pivotal|underscore|showcase|comprehensive|holistic|myriad|testament)\b",
    "inflated verb": r"\b(utilis|utiliz|leverag|facilitat|orchestrat)\w*\b",
    "borrowed term of art": r"\b(anaphora|ratif\w+|prima facie|a priori|dialectic\w*|teleolog\w+|epistemic|ipso facto|vis-?a-?vis|per se)\b",
    "latinate formality": r"\b(commenc\w+|ascertain\w*|endeavour\w*|obviate\w*|ameliorat\w+|requisite|aforementioned|heretofore|notwithstanding|delineat\w+|elucidat\w+|cognisant|cognizant|prior to|subsequent to|in the event that|a myriad of)\b",
    "hedge": r"\b(might potentially|may help to|can serve to|should generally|tends to be)\b",
    "transition stack": r"(?m)^(Furthermore|Moreover|Additionally|Ultimately)\b",
}

def sentences(text):
    prose = re.sub(r"```.*?```", "", text, flags=re.S)          # drop code blocks
    prose = re.sub(r"(?m)^\s*[-*|#>].*$", "", prose)             # drop lists/tables/headings
    return [s for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) > 2]

def report(path):
    text = pathlib.Path(path).read_text()
    words = len(text.split())
    sents = sentences(text)
    lens = [len(s.split()) for s in sents]
    print(f"\n=== {path}")
    print(f"words {words}   prose sentences {len(sents)}")
    if lens:
        mean = statistics.mean(lens)
        sd = statistics.pstdev(lens)
        print(f"sentence length mean {mean:.1f}  sd {sd:.1f}  burstiness {sd/mean:.2f}"
              f"   (human 0.6-1.2, machine 0.2-0.4)")
    em = text.count("—")
    print(f"em dashes {em}  ({em/max(words,1)*1000:.1f} per 1000 words; human 3.7-10, GPT-4 ~10.6)")
    for name, pat in TELLS.items():
        n = len(re.findall(pat, text, re.I))
        if n:
            print(f"  {name}: {n}")

for p in sys.argv[1:]:
    report(p)
