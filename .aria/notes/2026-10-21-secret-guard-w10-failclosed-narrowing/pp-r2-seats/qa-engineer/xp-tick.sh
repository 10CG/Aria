#!/usr/bin/env bash
# xp-tick.sh : V3-E5 (SECRET_GUARD_TIME_BUDGET_S=1) is exposed to the 1-second granularity of $SECONDS: if a wall-clock second boundary falls between the reset of the
# time-budget clock (start of _sg_vx_collect) and the first checkpoint of the BASELINE pass, the baseline pass itself emits the time text and the hook never reaches the
# trigger point. This sweeps the start phase (fraction of the second at which the hook is started) over the exact V3-E5 invocation and reports the text kind.
D=$(cd "$(dirname "$0")" && pwd); V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
python3 "$V/shapes.py" stall-read "$W/s.txt" && jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/s.txt" > "$W/s.json"
RJQ=$(command -v jq); RSED=$(command -v sed)
kind() { if grep -q 'within the time budget' "$1"; then echo TIME-TEXT; elif grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'too large to scan' "$1"; then echo oversize; elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
hook=${1:-$D/v31.sh}; bad=0; n=0
echo "# hook $(basename "$hook"), load $(cut -d' ' -f1-3 /proc/loadavg)"
for ph in 00 05 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95; do
  while :; do t=${EPOCHREALTIME/,/.}; f=${t#*.}; [[ ${f:0:2} == "$ph" ]] && break; sleep 0.004; done
  st=$(mktemp -d -p "$W"); t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR SC_SHIM_STATE="$st" SC_REAL_jq="$RJQ" SC_REAL_sed="$RSED" PATH="$V/shim:$PATH" SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=1 \
    taskset -c 0,1 nice -n 19 timeout 12 bash "$hook" < "$W/s.json" >/dev/null 2>"$W/e"; rc=$?; t1=$EPOCHREALTIME
  k=$(kind "$W/e"); n=$((n+1)); [[ $k == TIME-TEXT ]] && bad=$((bad+1))
  printf 'start phase .%s  rc=%s  %-9s wall=%.2fs\n' "$ph" "$rc" "$k" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{print b-a}')"
done
echo "# $bad of $n start phases gave the time text instead of the size text (V3-E5 wants the size text at 0.85..1.6 s)"
