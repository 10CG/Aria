#!/usr/bin/env bash
# usage: onemut.sh <label> <l1|l3> <variant> <WPA_ONLY> [WPA_ROWS]   -- one bad implementation, outside mutbatch (private work dir and private spec snapshot)
EXP=/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6
label=$1; kind=$2; variant=$3; only=$4; rows=${5:-}
export HOME=$EXP/home TMPDIR=$EXP/tmp
w=$EXP/work/one/$label; rm -rf "$w"; mkdir -p "$w/aria" "$w/spec"
cp -a "$EXP/work/t4f/aria/hooks" "$w/aria/hooks"; ln -s "$EXP/work/t4f/standards" "$w/standards"
if [ "$kind" = l1 ]; then python3 "$EXP/proto/patch_l1.py" "$EXP/base/aria/hooks/secret-guard.sh" "$w/aria/hooks/secret-guard.sh" --variant "$variant" >/dev/null || exit 3
else python3 "$EXP/proto/patch_l3.py" "$EXP/base/aria/hooks/secret-scan.sh" "$w/aria/hooks/secret-scan.sh" --variant "$variant" >/dev/null || exit 3; fi
cp "$EXP/spec/baseline_probe.py" "$EXP/spec/proposal.md" "$EXP/spec/baseline-evidence.md" "$w/spec/"
cd "$w/spec" || exit 1
unset WPA_BASH32
WPA_ONLY=$only WPA_ROWS=$rows python3 baseline_probe.py "$w/aria" 2>&1 | grep -E "^SC-[0-9]+ │" | awk -F' │ ' '{ if ($NF != "yes") print $1, $2, "->", $NF, "|", $(NF-1), "|", $(NF-2) }' | cut -c1-300
echo "rc-done $label"
