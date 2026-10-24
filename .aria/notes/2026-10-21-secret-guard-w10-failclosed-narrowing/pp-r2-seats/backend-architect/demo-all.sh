#!/usr/bin/env bash
# demo-all.sh : e2e demonstration of the behavioural difference of the mutants that sc-cases.sh does not catch (hook run by bash 5.2, nice, one run each).
D=$(cd "$(dirname "$0")" && pwd)
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth
  elif grep -q 'segments together are longer than' "$1"; then echo tmax; elif grep -q 'too large to scan' "$1"; then echo oversize
  elif grep -q 'within the time budget' "$1"; then echo time; elif grep -q 'value-REDACTING filter' "$1"; then echo finding
  elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
run1() {   # hook shape [env...]
  local h=$1 s=$2 e st t0 t1 rc; shift 2
  e=$(mktemp); st=$(mktemp -d)
  t0=$EPOCHREALTIME
  env -u CLAUDE_PROJECT_DIR SC_SHIM_STATE="$st" SC_REAL_jq="$(command -v jq)" SC_REAL_sed="$(command -v sed)" "$@" taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "$D/in2/$s.json" >/dev/null 2>"$e"; rc=$?
  t1=$EPOCHREALTIME
  printf '%-34s %-8s rc=%-3s %-9s %5.2fs bytes=%s sha=%s\n' "$s" "$(basename "$h" .sh)" "$rc" "$(kind "$e")" "$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{print b-a}')" "$(wc -c < "$e")" "$(sha256sum < "$e" | cut -c1-8)"
  rm -rf "$e" "$st"
}
echo "# load at start: $(cut -d' ' -f1-3 /proc/loadavg)"
echo "## M9/M10: growth > 8192 (whole / segment mode): block expected (growth text); mutants return 0 = ALLOW"
for s in growth-whole growth-seg; do for h in base v31 mut/M9 mut/M10; do run1 "$D/$h.sh" "$s"; done; done
echo "## M4/M11: single copy line > 8192 reading a protected file WITH a value-redacting filter: rows only -> block (longline) expected"
for s in seg-longline-filtered whole-longline-filtered seg-longline-plain; do for h in base v31 mut/M4 mut/M11; do run1 "$D/$h.sh" "$s"; done; done
echo "## M6: the LMAX boundary (longest copy line exactly 8192 -> normal text, 8193 -> longline)"
for s in lmax-8192 lmax-8193; do for h in base v31 mut/M6; do run1 "$D/$h.sh" "$s"; done; done
echo "## M5: segment-mode fallback (deadline cut): bytes must equal the baseline's"
for h in base v31 mut/M5; do run1 "$D/$h.sh" stall-read-seg "PATH=$V/shim:$PATH" SC_DELAY_sed=10; done
echo "# load at end: $(cut -d' ' -f1-3 /proc/loadavg)"
