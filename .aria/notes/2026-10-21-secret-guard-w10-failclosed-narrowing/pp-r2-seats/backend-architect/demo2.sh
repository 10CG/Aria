#!/usr/bin/env bash
D=$(cd "$(dirname "$0")" && pwd); V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth
  elif grep -q 'segments together are longer than' "$1"; then echo tmax; elif grep -q 'too large to scan' "$1"; then echo oversize
  elif grep -q 'within the time budget' "$1"; then echo time; elif grep -q 'value-REDACTING filter' "$1"; then echo finding
  elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
run1() { local h=$1 s=$2 e st t0 t1 rc; shift 2; e=$(mktemp); st=$(mktemp -d); t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR SC_SHIM_STATE="$st" SC_REAL_jq="$(command -v jq)" SC_REAL_sed="$(command -v sed)" "$@" taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "$D/in2/$s.json" >/dev/null 2>"$e"; rc=$?; t1=$EPOCHREALTIME
  printf '%-26s %-6s rc=%-3s %-9s %5.2fs bytes=%-5s sha=%s\n' "$s" "$(basename "$h" .sh)" "$rc" "$(kind "$e")" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{print b-a}')" "$(wc -c < "$e")" "$(sha256sum < "$e" | cut -c1-8)"; rm -rf "$e" "$st"; }
echo "# load at start: $(cut -d' ' -f1-3 /proc/loadavg)"
echo "## growth > 8192 (reader hidden behind \$f): baseline = oversize block; v3.1 = growth block; M9 (whole) / M10 (segment) = allow"
for s in growth-whole growth-seg; do for h in base v31 mut/M9 mut/M10; do run1 "$D/$h.sh" "$s"; done; done
echo "## M5: segment-mode deadline fallback must equal the baseline's bytes (baseline run WITHOUT the shim, hooks with sed stalling the job 10 s)"
run1 "$D/base.sh" seg-longline-plain
for h in v31 mut/M5; do run1 "$D/$h.sh" seg-longline-plain "PATH=$V/shim:$PATH" SC_DELAY_sed=10; done
echo "# load at end: $(cut -d' ' -f1-3 /proc/loadavg)"
