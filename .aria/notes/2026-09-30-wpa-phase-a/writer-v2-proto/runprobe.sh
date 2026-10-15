#!/usr/bin/env bash
# usage: runprobe.sh <label> <tree root (contains aria/ and standards/)> <spec dir> <b32: 0|1> [WPA_ONLY list]
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2
label=$1; tree=$2; spec=$3; b32=$4; only=${5:-}
export HOME=$EXP/home TMPDIR=$EXP/tmp
unset WPA_BASH32 WPA_ONLY
[ "$b32" = 1 ] && export WPA_BASH32=$EXP/bash32/bash-3.2/bash
[ -n "$only" ] && export WPA_ONLY=$only
cd "$spec" || exit 1
rm -f "$EXP/final/$label.rc"
python3 baseline_probe.py "$tree/aria" > "$EXP/final/$label.out" 2> "$EXP/final/$label.err"
echo "rc=$?" > "$EXP/final/$label.rc"
