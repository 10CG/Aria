#!/usr/bin/env bash
# sc27_concurrency.sh [copies] -- run the SC-27 rows of the probe in N concurrent copies on the SAME unpatched target tree; prints the actual column of 27b / 27c per copy.
# Purpose: tell concurrency noise (several probes running the two suites at once) from a real effect of a document variant.  Output: out/sc27_concurrency.txt
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
n=${1:-4}
cd "$EXP" || exit 1
export HOME=$EXP/home TMPDIR=$EXP/tmp
for i in $(seq 1 "$n"); do
  snap=$EXP/work/snap/c27_$i; rm -rf "$snap"; mkdir -p "$snap"
  cp spec/baseline_probe.py spec/proposal.md spec/baseline-evidence.md "$snap"/
  ( cd "$snap" && WPA_ONLY=SC-27 python3 baseline_probe.py "$EXP/work/t6/aria" 2>&1 | grep -E '^SC-27 │ 27[abcd] │' | awk -F' │ ' -v c="$i" '{print "copy " c ": " $2 " | " $(NF-1) " | " $NF}' > "$EXP/out/sc27_concurrency.$i" ) &
done
wait
cat "$EXP"/out/sc27_concurrency.[0-9]* > "$EXP/out/sc27_concurrency.txt"; rm -f "$EXP"/out/sc27_concurrency.[0-9]*
cat "$EXP/out/sc27_concurrency.txt"
