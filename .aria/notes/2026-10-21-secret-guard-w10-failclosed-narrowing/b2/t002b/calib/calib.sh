#!/usr/bin/env bash
# calib.sh HOOK : natural wall of a few e2e shapes (no shim), to size the timing classes
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
D=$(cd "$(dirname "$0")" && pwd); H=$1
for s in benign-big multiline-credit tmax-rerun count-axis count-axis-ctl longline-expansion stall-read; do
  python3 "$V/shapes.py" "$s" "$D/in/$s.txt"; jq -Rs '{tool_name:"Bash", tool_input:{command:.}}' < "$D/in/$s.txt" > "$D/in/$s.json"
done
echo "# load start $(cut -d' ' -f1-3 /proc/loadavg)"
for s in benign-big multiline-credit tmax-rerun count-axis count-axis-ctl longline-expansion stall-read; do
  for k in 1 2; do
    e=$(mktemp -p "$D"); t0=$EPOCHREALTIME
    env -u CLAUDE_PROJECT_DIR -u _SG_RELAXED -u SECRET_GUARD_TIME_BUDGET_S -u WSL_DISTRO_NAME -u WSL_INTEROP HOME="$D/home" taskset -c 0,1 nice -n 19 timeout 12 /usr/bin/bash "$H" < "$D/in/$s.json" >/dev/null 2>"$e"; rc=$?
    t1=$EPOCHREALTIME
    k1=$(grep -o 'has a line longer than\|grows by more than\|segments together are longer than\|too large to scan\|within the time budget\|value-REDACTING filter' "$e" | head -1)
    printf '%-20s rc=%s wall=%s kind=[%s] bytes=%s\n' "$s" "$rc" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')" "$k1" "$(wc -c < "$e")"
    rm -f "$e"
  done
done
echo "# load end $(cut -d' ' -f1-3 /proc/loadavg)"
