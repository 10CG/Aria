#!/usr/bin/env bash
# xp-ext.sh : consequence demos for M01 (stdin-cwd route of the extension) and M02 (segment-mode trigger point without the gate). Inputs are built at run time.
D=$(cd "$(dirname "$0")" && pwd); V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
BASE=$W/base.sh; git -C /home/dev/Aria/aria show 59e333c:hooks/secret-guard.sh > "$BASE"
mkdir -p "$W/ext/.aria"; printf '%s\n' "billing/conf/prod.toml" > "$W/ext/.aria/secret-guard.paths"
X4000=$(printf '%*s' 4000 '' | tr ' ' x); FILL=$(printf ' y%.0s' $(seq 1 2100))
# segment mode (no parenthesis): a big benign segment, then a read of the path the extension lists
printf '%s' "x=${X4000}; : \$x \$x${FILL}; cat /srv/billing/conf/prod.toml" > "$W/seg.txt"
# whole mode (parenthesis) with the project given ONLY through the stdin cwd
printf '%s' "(x=1; : \$x
$(printf 'A%.0s' $(seq 1 24000))
cat /srv/billing/conf/prod.toml)" > "$W/whole.txt"
jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/seg.txt" > "$W/seg.json"
jq -Rs --arg c "$W/ext" '{tool_name:"Bash", cwd:$c, tool_input:{command:.}}' < "$W/whole.txt" > "$W/whole-cwd.json"
run() { local h=$1 j=$2; shift 2; local t0=$EPOCHREALTIME; env -u CLAUDE_PROJECT_DIR "$@" taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "$W/$j" >/dev/null 2>"$W/err"; local rc=$?; local t1=$EPOCHREALTIME
  local k=none; if grep -q 'too large to scan' "$W/err"; then k=oversize-text; elif [[ -s "$W/err" ]]; then k=other-text; fi
  printf 'rc=%s %-13s wall=%.2fs\n' "$rc" "$k" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{print b-a}')"; }
echo "== A. segment mode, project via CLAUDE_PROJECT_DIR (extension lists the path that is read) =="
echo -n "baseline : "; run "$BASE" seg.json CLAUDE_PROJECT_DIR="$W/ext"
echo -n "v3.1 good: "; run "$D/v31.sh" seg.json CLAUDE_PROJECT_DIR="$W/ext"
echo -n "M02      : "; run "$D/mut/M02.sh" seg.json CLAUDE_PROJECT_DIR="$W/ext"
echo "== B. whole mode, project via the stdin cwd only (no CLAUDE_PROJECT_DIR) =="
echo -n "baseline : "; run "$BASE" whole-cwd.json
echo -n "v3.1 good: "; run "$D/v31.sh" whole-cwd.json
echo -n "M01      : "; run "$D/mut/M01.sh" whole-cwd.json
