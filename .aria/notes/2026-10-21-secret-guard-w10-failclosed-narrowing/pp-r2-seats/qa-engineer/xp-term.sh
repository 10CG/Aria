#!/usr/bin/env bash
# xp-term.sh <mutant ids...> : the deadline cases run the hook with default signal dispositions. A harness that starts the hook with SIGTERM ignored (inherited across fork / exec)
# makes a TERM-based deadline a no-op. Same invocation as V6-E2 (stall-read, the sed shim stalls the job for 10 s), started with `trap '' TERM`.
D=$(cd "$(dirname "$0")" && pwd); V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
python3 "$V/shapes.py" stall-read "$W/s.txt" && jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$W/s.txt" > "$W/s.json"
RJQ=$(command -v jq); RSED=$(command -v sed)
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'too large to scan' "$1"; then echo oversize; elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
printf '#!/bin/bash\ntrap "" TERM\nexec bash "$1"\n' > "$W/termwrap.sh"
for h in "$D/v31.sh" $(for m in "$@"; do echo "$D/mut/$m.sh"; done); do
  for mode in default term-ignored; do
    st=$(mktemp -d -p "$W"); t0=$EPOCHREALTIME
    if [[ $mode == default ]]; then wrap=(bash "$h"); else wrap=(bash "$W/termwrap.sh" "$h"); fi
    env -u CLAUDE_PROJECT_DIR SC_SHIM_STATE="$st" SC_REAL_jq="$RJQ" SC_REAL_sed="$RSED" PATH="$V/shim:$PATH" SC_DELAY_sed=10 \
      taskset -c 0,1 nice -n 19 timeout -s KILL 14 "${wrap[@]}" < "$W/s.json" >/dev/null 2>"$W/e"; rc=$?; t1=$EPOCHREALTIME
    printf '%-8s %-12s rc=%s %-9s wall=%.2fs\n' "$(basename "$h" .sh)" "$mode" "$rc" "$(kind "$W/e")" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{print b-a}')"
  done
done
