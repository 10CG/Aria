#!/usr/bin/env bash
# run-w9.sh <aria hooks dir at the baseline> <work dir> [--reduce-only] : runs hooks/tests/secret-guard.test.sh on a copy with the baseline hook and on a copy
# with the v3 prototype (same conditions: the copies are not git checkouts, so the cases that read an old hook through `git show` do not run in either),
# then writes W9-suite.txt: totals, and every failing case with its failing checks; command excerpts inside [...] are masked.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; HK=$1; W=$2
if [[ "${3:-}" != --reduce-only ]]; then
  for t in base v3; do rm -rf "$W/tree-$t"; mkdir -p "$W/tree-$t"; cp -r "$HK" "$W/tree-$t/hooks"; done
  python3 "$HERE/mkv3.py" "$HK/secret-guard.sh" "$W/tree-v3/hooks/secret-guard.sh" >/dev/null || exit 1
  for t in base v3; do taskset -c 0,1 nice -n 19 bash "$W/tree-$t/hooks/tests/secret-guard.test.sh" > "$W/suite-$t.out" 2>&1; done
fi
{ printf '# suite outputs: %s (base) / %s (v3) | v3 hook sha256 %s\n' "$(date -u -r "$W/suite-base.out" +%FT%TZ)" "$(date -u -r "$W/suite-v3.out" +%FT%TZ)" "$(sha256sum < "$W/tree-v3/hooks/secret-guard.sh" | cut -c1-12)"
  for t in base v3; do echo "## $t"; grep -E '^(PASS|FAIL):' "$W/suite-$t.out"
    grep -E '^  FAIL \[' "$W/suite-$t.out" | python3 -c '
import sys, re
for ln in sys.stdin:
    m = re.match(r"  FAIL \[(.*?)\]: (.*)", ln.rstrip("\n"))
    name, body = m.group(1), m.group(2)
    print("  FAIL", name[:110])
    for chk in re.findall(r"\{(.*?)\}(?= \{|$)", body):
        chk = re.sub(r"\[[^\]]*\]", "[...]", chk, count=1)
        print("     ", chk[:220])
    if not body.startswith(tuple("0123456789")): print("     ", re.sub(r"\[[^\]]*\]", "[...]", body)[:220])
'; done; } > "$HERE/W9-suite.txt"
echo done
