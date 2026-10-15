#!/usr/bin/env bash
# Full prototype tree whose secret-scan suite has the `Coverage: K cases` header comment but NOT the self-check assertion (SC-27 27d bad implementation).
# usage: build_noselfcheck.sh <out dir>
set -eu
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4
out=$1
rm -rf "$out" && mkdir -p "$out"
cp -a "$EXP/base/aria" "$out/aria" && cp -a "$EXP/base/standards" "$out/standards"
python3 "$EXP/proto/patch_l3.py" "$EXP/base/aria/hooks/secret-scan.sh" "$out/aria/hooks/secret-scan.sh" --variant v4 >/dev/null
python3 "$EXP/proto/patch_l1.py" "$EXP/base/aria/hooks/secret-guard.sh" "$out/aria/hooks/secret-guard.sh" --variant v4 >/dev/null
python3 "$EXP/proto/patch_docs.py" "$out" >/dev/null
python3 "$EXP/proto/patch_tests.py" "$out" "$out/aria/hooks/secret-scan.sh" --family-count 64 --no-selfcheck >/dev/null
echo built "$out" "(no self-check)"
