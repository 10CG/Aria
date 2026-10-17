#!/usr/bin/env python3
"""xref_check.py PROPOSAL STDOUT -- cross-reference check between the Spec text and the probe output.

1. every row id the text cites (`4p`, `22bk`, `7h / 7j`, range ends such as `11m–11r`) exists in the probe output (any SC);
   the check is per SC bullet and "SC-n xx" pairs: an id cited as `SC-22 22av` must exist under SC-22;
2. every row id in the probe output is cited somewhere in the text (a row nobody describes is a row nobody can review);
3. every count claim `(`category` ×N`) and `基线 a/b` is printed so a human can compare with the stdout tallies (done by the caller).
"""
import re
import sys

prop = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], encoding="utf-8").read()
rows = {}
for l in out.split("\n"):
    m = re.match(r"^(SC-(\d+)) │ (\S+) │ (\S+) │ ", l)
    if m:
        rows[(int(m.group(2)), m.group(3))] = m.group(4)
ids_by_num = {}
for (n, cid) in rows:
    ids_by_num.setdefault(n, set()).add(cid)
all_ids = {cid for (_n, cid) in rows}
WHITELIST = {"1e", "1a"}   # `1e-4` style magnitudes
cited = set()
bad = []
for m in re.finditer(r"(?<![A-Za-z0-9_`./-])(\d{1,2})([a-z]{1,2}|[A-Z])(?![A-Za-z0-9_])", prop):
    tok = m.group(0)
    ctx = prop[max(0, m.start() - 25): m.end() + 15].replace("\n", " ")
    if tok in ("1e",):
        continue
    cited.add(tok)
    if tok not in all_ids:
        bad.append((tok, ctx))
print("tokens cited:", len(cited), "| not a row id:", len(bad))
for tok, ctx in bad:
    print("  NOT A ROW:", tok, "|", ctx)
uncited = sorted(all_ids - cited, key=lambda x: (int(re.match(r"\d+", x).group(0)), x))
print("rows never cited in the text:", len(uncited))
print(" ", " ".join(uncited))
# per-bullet SC pairs: `SC-22 22av`
pairs = re.findall(r"SC-(\d+) (\d{1,2}[a-zA-Z]{1,2})", prop)
wrong = [(sc, cid) for sc, cid in pairs if cid not in ids_by_num.get(int(sc), set())]
print("`SC-n id` pairs:", len(pairs), "| id not under that SC:", len(wrong))
for sc, cid in wrong:
    print("  WRONG PAIR: SC-%s %s" % (sc, cid))
