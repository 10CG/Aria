#!/usr/bin/env bash
# Build the full target-state PROTOTYPE tree (hooks + docs + test suites) from the baseline copies.
# usage: build_full.sh <out dir> [family_count]      (prototype of the design, not the implementation)
set -eu
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
out=$1; fam=${2:-64}
rm -rf "$out" && mkdir -p "$out"
cp -a "$EXP/aria" "$out/aria" && cp -a "$EXP/standards" "$out/standards"
python3 "$EXP/proto/patch_l3.py" "$EXP/aria/hooks/secret-scan.sh" "$out/aria/hooks/secret-scan.sh"
python3 "$EXP/proto/patch_l1.py" "$EXP/aria/hooks/secret-guard.sh" "$out/aria/hooks/secret-guard.sh"
python3 "$EXP/proto/patch_docs.py" "$out"
python3 "$EXP/proto/patch_tests.py" "$out" "$out/aria/hooks/secret-scan.sh" --family-count "$fam"
