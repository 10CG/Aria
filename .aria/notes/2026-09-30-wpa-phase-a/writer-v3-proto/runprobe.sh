#!/usr/bin/env bash
# usage: runprobe.sh <label> <tree root (contains aria/ and standards/)> <spec dir> <b32: 0|1> [WPA_ONLY list]
# The spec dir (probe + proposal + evidence) is snapshotted first, so editing it while a run is in flight cannot change that run.
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b
label=$1; tree=$2; spec=$3; b32=$4; only=${5:-}
export HOME=$EXP/home TMPDIR=$EXP/tmp
unset WPA_BASH32 WPA_ONLY
[ "$b32" = 1 ] && export WPA_BASH32=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v3b/bash32/bash
[ -n "$only" ] && export WPA_ONLY=$only
[ -n "$WPA_REQUIRE_ALL_PASS" ] && export WPA_REQUIRE_ALL=1
snap="$EXP/work/snap/$label"; rm -rf "$snap"; mkdir -p "$snap" "$EXP/logs"
cp "$spec"/baseline_probe.py "$spec"/proposal.md "$spec"/baseline-evidence.md "$snap"/ 2>/dev/null
cd "$snap" || exit 1
rm -f "$EXP/logs/$label.rc"
python3 baseline_probe.py "$tree/aria" > "$EXP/logs/$label.out" 2> "$EXP/logs/$label.err"
echo "rc=$?" > "$EXP/logs/$label.rc"
