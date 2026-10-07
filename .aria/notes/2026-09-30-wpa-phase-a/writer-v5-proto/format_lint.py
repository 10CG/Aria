#!/usr/bin/env python3
"""format_lint.py FILE [...] -- the discipline checks of the repair dispatch, mechanically: LF line ends, no tab, no circled / enclosed digits, no emoji, no AI attribution line, no bare issue
reference (`#123` not preceded by an org/repo name; `Rule #7` style rule references are not issue references), and -- for proposal.md only -- no version / audit narrative in the body
(`writer-v<N>` other than the archive path `writer-v5-proto`, `v3` / `v4` as a round name, `上两轮`, `本版`, `曾写`, `曾全绿`, `曾在`, `返修`) and Status line = the one allowed sentence.
Prints one line per check and the offending lines (first 60 characters of context only); exit 1 if anything is found."""
import re
import sys

bad = 0
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    lines = t.split("\n")
    res = []
    res.append(("CR characters", t.count("\r")))
    res.append(("tab characters", t.count("\t") if not path.endswith((".tsv", ".sh")) else 0))
    res.append(("circled / enclosed digits", len(re.findall(r"[①-⓿❶-➓㉈-㉏]", t))))
    res.append(("emoji", len(re.findall(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]", t))))
    res.append(("AI attribution lines", sum(1 for l in lines if re.search(r"Co-Authored-By|Generated with|noreply@anthropic", l))))
    bare = [(i, l[max(0, m.start() - 20): m.end() + 10]) for i, l in enumerate(lines, 1) for m in re.finditer(r"(?<![A-Za-z0-9_./-])#(\d{2,4})\b", l) if not re.search(r"Rule\s*$", l[:m.start()])]
    res.append(("bare issue references", len(bare)))
    narr = []
    if path.endswith("proposal.md"):
        for i, l in enumerate(lines, 1):
            for p in (r"writer-v(?!5-proto)\d", r"\bv[34]\b", "上两轮", "本版", "曾写", "曾全绿", "曾在", "返修"):
                for m in re.finditer(p, l):
                    narr.append((i, l[max(0, m.start() - 20): m.end() + 20]))
        st = [l for l in lines if l.startswith("> **Status**")]
        res.append(("Status line is `Draft — post_spec 审计中`", 0 if st == ["> **Status**: Draft — post_spec 审计中"] else 1))
        res.append(("version / audit narrative in the body", len(narr)))
    print(f"{path}: " + "; ".join(f"{k}={v}" for k, v in res))
    for i, c in bare[:10]:
        print(f"   bare issue ref line {i}: ...{c}...")
    for i, c in narr[:10]:
        print(f"   narrative line {i}: ...{c}...")
    bad += sum(v for _k, v in res) + 0
sys.exit(1 if bad else 0)
