#!/usr/bin/env bash
# Build a FULL tree whose DOCUMENTATION is patched with a bad variant (SC-26 / SC-28 rows read standards, README, CHANGELOG, VERSION and the hook headers).
# usage: build_docvariant.sh <out dir> <patch_docs.py flag, e.g. --hdr-count | --hdr-half-l | --hdr-dangling | --bad-sot | --bad | --bad-layer | --no-scope>
# The hooks and the test suites are the v4 prototype (so only the document rows can differ).
set -eu
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4
out=$1; flag=$2
rm -rf "$out" && mkdir -p "$out"
cp -a "$EXP/base/aria" "$out/aria" && cp -a "$EXP/base/standards" "$out/standards"
python3 "$EXP/proto/patch_l3.py" "$EXP/base/aria/hooks/secret-scan.sh" "$out/aria/hooks/secret-scan.sh" --variant v4 >/dev/null
python3 "$EXP/proto/patch_l1.py" "$EXP/base/aria/hooks/secret-guard.sh" "$out/aria/hooks/secret-guard.sh" --variant v4 >/dev/null
python3 "$EXP/proto/patch_docs.py" "$out" "$flag" >/dev/null
python3 "$EXP/proto/patch_tests.py" "$out" "$out/aria/hooks/secret-scan.sh" --family-count 64 >/dev/null
echo built "$out" "($flag)"
